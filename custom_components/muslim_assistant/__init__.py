"""Muslim Assistant - Home Assistant Integration.

A comprehensive Islamic companion integration providing prayer times,
Qibla direction, Hijri calendar, Quran verses, daily Duas, Ramadan
tracking, and more.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import MuslimAssistantCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Muslim Assistant from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = MuslimAssistantCoordinator(
        hass,
        latitude=entry.data.get(CONF_LATITUDE, hass.config.latitude),
        longitude=entry.data.get(CONF_LONGITUDE, hass.config.longitude),
        calc_method=entry.data.get("calculation_method", "ISNA"),
        school=entry.data.get("school", "Standard"),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    await async_setup_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up Muslim Assistant services."""
    from .services import async_register_services

    await async_register_services(hass)
