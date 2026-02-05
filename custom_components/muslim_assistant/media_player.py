"""Media player platform for Muslim Assistant integration.

Provides a virtual media player entity that proxies Adhan and Quran audio
to any Home Assistant media player (Alexa, Google Home, Sonos, etc.).
"""

from __future__ import annotations

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
    QURAN_RECITERS,
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
    it forwards the audio URL to the user's configured target media player
    (e.g., an Alexa Echo, Google Home speaker, or Sonos).
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
        target = self._entry.options.get(CONF_TARGET_PLAYER, "")
        return {
            "quran_reciter": reciter,
            "target_media_player": target,
        }

    def _get_target_entity_id(self) -> str | None:
        """Get the target media player entity ID from options."""
        return self._entry.options.get(CONF_TARGET_PLAYER) or None

    async def _forward_to_target(
        self, service: str, data: dict[str, Any] | None = None
    ) -> None:
        """Forward a media_player service call to the target speaker."""
        target = self._get_target_entity_id()
        if not target:
            _LOGGER.warning(
                "No target media player configured. "
                "Go to Muslim Assistant > Configure > Audio Settings "
                "and set your speaker entity (e.g., media_player.living_room_echo)"
            )
            return

        service_data = {"entity_id": target}
        if data:
            service_data.update(data)

        try:
            await self.hass.services.async_call(
                "media_player",
                service,
                service_data,
                blocking=True,
            )
        except Exception as err:
            _LOGGER.error("Error calling %s on %s: %s", service, target, err)

    async def async_play_media(
        self,
        media_type: MediaType | str,
        media_id: str,
        **kwargs: Any,
    ) -> None:
        """Play media on the target device."""
        self._media_content_id = media_id
        self._state = MediaPlayerState.PLAYING
        self.async_write_ha_state()

        await self._forward_to_target(
            "play_media",
            {
                "media_content_id": media_id,
                "media_content_type": media_type
                if isinstance(media_type, str)
                else media_type.value,
            },
        )

    async def async_media_play(self) -> None:
        """Resume playback on the target device."""
        if self._media_content_id:
            self._state = MediaPlayerState.PLAYING
            self.async_write_ha_state()
            await self._forward_to_target("media_play")

    async def async_media_pause(self) -> None:
        """Pause playback on the target device."""
        self._state = MediaPlayerState.PAUSED
        self.async_write_ha_state()
        await self._forward_to_target("media_pause")

    async def async_media_stop(self) -> None:
        """Stop the media player."""
        self._state = MediaPlayerState.IDLE
        self._media_title = None
        self._media_artist = None
        self._media_content_id = None
        self.async_write_ha_state()
        await self._forward_to_target("media_stop")

    async def async_play_adhan(self) -> None:
        """Play the Adhan audio."""
        url = self.coordinator.get_adhan_audio_url()
        self._media_title = "Adhan"
        self._media_artist = "Muslim Assistant"
        await self.async_play_media(MediaType.MUSIC, url)

    async def async_play_quran(
        self, surah: int, ayah: int | None = None
    ) -> None:
        """Play Quran audio for a surah or ayah."""
        url = self.coordinator.get_quran_audio_url(surah, ayah)
        reciter = self._entry.options.get(
            CONF_QURAN_RECITER, DEFAULT_RECITER
        )
        self._media_title = (
            f"Surah {surah}" if ayah is None else f"Surah {surah}:{ayah}"
        )
        self._media_artist = reciter
        await self.async_play_media(MediaType.MUSIC, url)
