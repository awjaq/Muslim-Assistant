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

    async def async_play_media(
        self,
        media_type: MediaType | str,
        media_id: str,
        **kwargs: Any,
    ) -> None:
        """Play media on the target device.

        media_id should be a direct URL to an audio file (MP3).
        Extra kwargs can include:
          - title: display title
          - artist: display artist name
        """
        self._media_content_id = media_id
        self._media_title = kwargs.get("extra", {}).get("title", "Muslim Assistant")
        self._media_artist = kwargs.get("extra", {}).get("artist", "")
        self._state = MediaPlayerState.PLAYING

        target = self._get_target_entity_id()
        if target:
            # Forward to the user's chosen media player
            await self.hass.services.async_call(
                "media_player",
                "play_media",
                {
                    "entity_id": target,
                    "media_content_id": media_id,
                    "media_content_type": "music",
                },
                blocking=True,
            )
        else:
            _LOGGER.warning(
                "No target media player configured. "
                "Set one in Muslim Assistant options to play audio on a speaker"
            )

        self.async_write_ha_state()

    async def async_media_stop(self) -> None:
        """Stop the media player."""
        self._state = MediaPlayerState.IDLE
        self._media_title = None
        self._media_artist = None
        self._media_content_id = None

        target = self._get_target_entity_id()
        if target:
            await self.hass.services.async_call(
                "media_player",
                "media_stop",
                {"entity_id": target},
                blocking=True,
            )

        self.async_write_ha_state()

    async def async_play_adhan(self) -> None:
        """Play the Adhan audio."""
        url = self.coordinator.get_adhan_audio_url()
        await self.async_play_media(
            MediaType.MUSIC,
            url,
            extra={"title": "Adhan", "artist": "Muslim Assistant"},
        )

    async def async_play_quran(
        self, surah: int, ayah: int | None = None
    ) -> None:
        """Play Quran audio for a surah or ayah."""
        url = self.coordinator.get_quran_audio_url(surah, ayah)
        reciter = self._entry.options.get(
            CONF_QURAN_RECITER, DEFAULT_RECITER
        )
        title = f"Surah {surah}" if ayah is None else f"Surah {surah}:{ayah}"
        await self.async_play_media(
            MediaType.MUSIC,
            url,
            extra={"title": title, "artist": reciter},
        )
