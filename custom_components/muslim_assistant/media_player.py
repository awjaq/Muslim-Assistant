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
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_QURAN_RECITER,
    CONF_TARGET_PLAYER,
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

    async def _forward_to_targets(
        self, service: str, data: dict[str, Any] | None = None
    ) -> None:
        """Forward a media_player service call to ALL target speakers."""
        targets = self._get_target_entity_ids()
        if not targets:
            _LOGGER.warning(
                "No target media players configured. "
                "Go to Muslim Assistant > Configure > Audio Settings "
                "and select your speakers."
            )
            return

        # Call service on all targets simultaneously
        tasks = []
        for target in targets:
            service_data = {"entity_id": target}
            if data:
                service_data.update(data)
            tasks.append(
                self.hass.services.async_call(
                    "media_player",
                    service,
                    service_data,
                    blocking=True,
                )
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                _LOGGER.error(
                    "Error calling %s on %s: %s",
                    service,
                    targets[i],
                    result,
                )

    async def async_play_media(
        self,
        media_type: MediaType | str,
        media_id: str,
        **kwargs: Any,
    ) -> None:
        """Play media on all target devices."""
        self._media_content_id = media_id
        self._state = MediaPlayerState.PLAYING
        self.async_write_ha_state()

        await self._forward_to_targets(
            "play_media",
            {
                "media_content_id": media_id,
                "media_content_type": media_type
                if isinstance(media_type, str)
                else media_type.value,
            },
        )

    async def async_media_play(self) -> None:
        """Resume playback on all target devices."""
        if self._media_content_id:
            self._state = MediaPlayerState.PLAYING
            self.async_write_ha_state()
            await self._forward_to_targets("media_play")

    async def async_media_pause(self) -> None:
        """Pause playback on all target devices."""
        self._state = MediaPlayerState.PAUSED
        self.async_write_ha_state()
        await self._forward_to_targets("media_pause")

    async def async_media_stop(self) -> None:
        """Stop all target media players."""
        self._state = MediaPlayerState.IDLE
        self._media_title = None
        self._media_artist = None
        self._media_content_id = None
        self.async_write_ha_state()
        await self._forward_to_targets("media_stop")

    async def async_play_adhan(self) -> None:
        """Play the Adhan audio on all targets."""
        url = self.coordinator.get_adhan_audio_url()
        self._media_title = "Adhan"
        self._media_artist = "Muslim Assistant"
        await self.async_play_media(MediaType.MUSIC, url)

    async def async_play_quran(
        self, surah: int, ayah: int | None = None
    ) -> None:
        """Play Quran audio on all targets."""
        url = self.coordinator.get_quran_audio_url(surah, ayah)
        reciter = self._entry.options.get(
            CONF_QURAN_RECITER, DEFAULT_RECITER
        )
        self._media_title = (
            f"Surah {surah}" if ayah is None else f"Surah {surah}:{ayah}"
        )
        self._media_artist = reciter
        await self.async_play_media(MediaType.MUSIC, url)
