"""Media player platform for Muslim Assistant integration.

Provides a virtual media player entity that proxies Adhan and Quran audio
to any Home Assistant media player (Alexa, Google Home, Sonos, phones, etc.).
Supports multiple target devices simultaneously.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ALEXA_MODE_ANNOUNCE,
    ALEXA_MODE_ROUTINE,
    ALEXA_PLATFORMS,
    CONF_ALEXA_MODE,
    CONF_ALEXA_ROUTINE,
    CONF_QURAN_RECITER,
    CONF_TARGET_PLAYER,
    DEFAULT_ALEXA_MODE,
    DEFAULT_RECITER,
    DOMAIN,
    VERSION,
)
from .coordinator import MuslimAssistantCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Muslim Assistant media player."""
    coordinator: MuslimAssistantCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MuslimAssistantMediaPlayer(coordinator, entry)])


class MuslimAssistantMediaPlayer(MediaPlayerEntity):
    """Media player entity for Adhan and Quran audio.

    This entity acts as a controller. When you call play_media on it,
    it forwards the audio URL to ALL configured target media players
    (e.g., Alexa, Google Home, Sonos, phones via companion app).
    """

    _attr_has_entity_name = True
    _attr_name = "Audio Player"
    _attr_device_class = MediaPlayerDeviceClass.SPEAKER
    _attr_supported_features = (
        MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.STOP
        | MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.PLAY_MEDIA
    )
    _attr_media_content_type = MediaType.MUSIC

    def __init__(
        self,
        coordinator: MuslimAssistantCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the media player."""
        self.coordinator = coordinator
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_media_player"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Muslim Assistant",
            "manufacturer": "Muslim Assistant Community",
            "model": "Islamic Companion",
            "sw_version": VERSION,
        }
        self._state = MediaPlayerState.IDLE
        self._media_title: str | None = None
        self._media_artist: str | None = None
        self._media_content_id: str | None = None

    @property
    def state(self) -> MediaPlayerState:
        """Return the state of the media player."""
        return self._state

    @property
    def media_title(self) -> str | None:
        """Return the title of current playing media."""
        return self._media_title

    @property
    def media_artist(self) -> str | None:
        """Return the artist of current playing media."""
        return self._media_artist

    @property
    def media_content_id(self) -> str | None:
        """Return the content ID of current playing media."""
        return self._media_content_id

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        reciter = self._entry.options.get(
            CONF_QURAN_RECITER, DEFAULT_RECITER
        )
        targets = self._get_target_entity_ids()
        return {
            "quran_reciter": reciter,
            "target_media_players": targets,
            "target_count": len(targets),
        }

    def _get_target_entity_ids(self) -> list[str]:
        """Get all target media player entity IDs from options."""
        targets = self._entry.options.get(CONF_TARGET_PLAYER, [])
        # Handle backward compatibility: old format was a single string
        if isinstance(targets, str):
            return [targets] if targets else []
        if isinstance(targets, list):
            return [t for t in targets if t]
        return []

    def _is_alexa(self, entity_id: str) -> bool:
        """Return True if the entity is an Amazon Echo / Alexa device."""
        entry = er.async_get(self.hass).async_get(entity_id)
        return bool(entry and entry.platform in ALEXA_PLATFORMS)

    def _split_targets(self) -> tuple[list[str], list[str]]:
        """Split targets into (regular players, Alexa devices)."""
        regular: list[str] = []
        alexa: list[str] = []
        for target in self._get_target_entity_ids():
            (alexa if self._is_alexa(target) else regular).append(target)
        return regular, alexa

    async def _call_all(self, calls: list[tuple[str, str, dict[str, Any]]]) -> None:
        """Run service calls in parallel, logging failures per call."""
        if not calls:
            return
        results = await asyncio.gather(
            *(
                self.hass.services.async_call(domain, service, data, blocking=True)
                for domain, service, data in calls
            ),
            return_exceptions=True,
        )
        for (domain, service, data), result in zip(calls, results):
            if isinstance(result, Exception):
                _LOGGER.error(
                    "Error calling %s.%s for %s: %s",
                    domain,
                    service,
                    data.get("entity_id") or data.get("target"),
                    result,
                )

    async def _forward_to_targets(
        self,
        service: str,
        data: dict[str, Any] | None = None,
        targets: list[str] | None = None,
    ) -> None:
        """Forward a media_player service call to target speakers."""
        if targets is None:
            targets = self._get_target_entity_ids()
        if not targets:
            return
        await self._call_all(
            [
                ("media_player", service, {"entity_id": t, **(data or {})})
                for t in targets
            ]
        )

    async def _handle_alexa(
        self, alexa: list[str], announcement: str | None, is_adhan: bool
    ) -> None:
        """Handle Alexa targets without sending them an audio URL.

        Echo devices cannot stream arbitrary MP3 URLs via play_media -- Alexa
        treats the URL as a voice search and replies "I can't play that".
        """
        if not alexa:
            return
        mode = self._entry.options.get(CONF_ALEXA_MODE, DEFAULT_ALEXA_MODE)

        if mode == ALEXA_MODE_ROUTINE:
            routine = (self._entry.options.get(CONF_ALEXA_ROUTINE) or "").strip()
            if not is_adhan or not routine:
                _LOGGER.debug("No Alexa routine for this audio; skipping Alexa")
                return
            await self._forward_to_targets(
                "play_media",
                {"media_content_id": routine, "media_content_type": "routine"},
                alexa,
            )
            return

        if mode == ALEXA_MODE_ANNOUNCE and announcement:
            if not self.hass.services.has_service("notify", "alexa_media"):
                _LOGGER.warning(
                    "Alexa announce needs the Alexa Media Player integration "
                    "(notify.alexa_media not found); skipping Alexa devices"
                )
                return
            await self._call_all(
                [
                    (
                        "notify",
                        "alexa_media",
                        {
                            "message": announcement,
                            "target": alexa,
                            "data": {"type": "announce"},
                        },
                    )
                ]
            )
        # ALEXA_MODE_SKIP (or nothing to announce): leave Alexa silent.

    async def _play_on_targets(
        self,
        url: str,
        announcement: str | None = None,
        is_adhan: bool = False,
    ) -> None:
        """Stream the URL to regular players; handle Alexa separately."""
        regular, alexa = self._split_targets()
        if not regular and not alexa:
            _LOGGER.warning(
                "No target media players configured. "
                "Go to Muslim Assistant > Configure > Audio Settings "
                "and select your speakers."
            )
            return
        self._media_content_id = url
        self._state = MediaPlayerState.PLAYING
        self.async_write_ha_state()
        await asyncio.gather(
            self._forward_to_targets(
                "play_media",
                {
                    "media_content_id": url,
                    "media_content_type": MediaType.MUSIC.value,
                },
                regular,
            ),
            self._handle_alexa(alexa, announcement, is_adhan),
        )

    async def async_play_media(
        self,
        media_type: MediaType | str,
        media_id: str,
        **kwargs: Any,
    ) -> None:
        """Play media on all target devices (Alexa handled separately)."""
        await self._play_on_targets(media_id)

    async def async_media_play(self) -> None:
        """Resume playback on all target devices."""
        if self._media_content_id:
            self._state = MediaPlayerState.PLAYING
            self.async_write_ha_state()
            await self._forward_to_targets(
                "media_play", targets=self._split_targets()[0]
            )

    async def async_media_pause(self) -> None:
        """Pause playback on all target devices."""
        self._state = MediaPlayerState.PAUSED
        self.async_write_ha_state()
        await self._forward_to_targets(
            "media_pause", targets=self._split_targets()[0]
        )

    async def async_media_stop(self) -> None:
        """Stop all target media players."""
        self._state = MediaPlayerState.IDLE
        self._media_title = None
        self._media_artist = None
        self._media_content_id = None
        self.async_write_ha_state()
        await self._forward_to_targets(
            "media_stop", targets=self._split_targets()[0]
        )

    async def async_play_adhan(self, prayer: str | None = None) -> None:
        """Play the Adhan audio on all targets."""
        url = self.coordinator.get_adhan_audio_url()
        self._media_title = f"Adhan - {prayer}" if prayer else "Adhan"
        self._media_artist = "Muslim Assistant"
        announcement = (
            f"It is time for {prayer} prayer." if prayer else "It is time for prayer."
        )
        await self._play_on_targets(url, announcement, is_adhan=True)

    async def async_play_quran(
        self, surah: int, ayah: int | None = None
    ) -> None:
        """Play Quran audio on all targets.

        Alexa devices are skipped: they cannot stream the recitation URL.
        """
        url = self.coordinator.get_quran_audio_url(surah, ayah)
        reciter = self._entry.options.get(
            CONF_QURAN_RECITER, DEFAULT_RECITER
        )
        self._media_title = (
            f"Surah {surah}" if ayah is None else f"Surah {surah}:{ayah}"
        )
        self._media_artist = reciter
        await self._play_on_targets(url)
