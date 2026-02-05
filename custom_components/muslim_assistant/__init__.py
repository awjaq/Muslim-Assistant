"""Muslim Assistant - Home Assistant Integration.

A comprehensive Islamic companion integration providing prayer times,
Qibla direction, Hijri calendar, Quran verses, daily Duas, Ramadan
tracking, Adhan and Quran audio playback, and more.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant

from .const import CONF_CALC_METHOD, CONF_SCHOOL, DOMAIN, PLATFORMS
from .coordinator import MuslimAssistantCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Muslim Assistant from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = MuslimAssistantCoordinator(
        hass,
        entry=entry,
        latitude=entry.data.get(CONF_LATITUDE, hass.config.latitude),
        longitude=entry.data.get(CONF_LONGITUDE, hass.config.longitude),
        calc_method=entry.data.get(CONF_CALC_METHOD, "ISNA"),
        school=entry.data.get(CONF_SCHOOL, "Standard"),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    from .services import async_register_services

    await async_register_services(hass)

    # Listen for options updates to reload coordinator
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_update_options(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Handle options update - reload the integration."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(
    hass: HomeAssistant, entry: ConfigEntry
) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
