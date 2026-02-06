"""Muslim Assistant - Home Assistant Integration.

A comprehensive Islamic companion integration providing prayer times,
Qibla direction, Hijri calendar, Quran verses, daily Duas, Ramadan
tracking, Adhan and Quran audio playback, and more.
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, EVENT_HOMEASSISTANT_STARTED
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

    # Auto-create dashboard (after HA is fully started)
    async def _on_started(event):
        await _async_create_dashboard(hass)

    if hass.is_running:
        await _async_create_dashboard(hass)
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _on_started)

    return True


async def _async_create_dashboard(hass: HomeAssistant) -> None:
    """Create the Muslim Assistant Lovelace dashboard automatically."""
    try:
        lovelace_data = hass.data.get("lovelace")
        if not lovelace_data:
            _LOGGER.debug("Lovelace not loaded, skipping dashboard auto-creation")
            return

        # Use attribute access (required for HA 2025+)
        dashboards = getattr(lovelace_data, "dashboards", None)
        if dashboards is None:
            return

        # Check if our dashboard already exists
        if "muslim-assistant" in dashboards:
            _LOGGER.debug("Muslim Assistant dashboard already exists")
            return

        collection = getattr(lovelace_data, "dashboards_collection", None)
        if collection is None:
            return

        # Create the dashboard entry
        await collection.async_create_item(
            {
                "url_path": "muslim-assistant",
                "title": "Muslim Assistant",
                "icon": "mdi:mosque",
                "show_in_sidebar": True,
                "require_admin": False,
                "mode": "storage",
            }
        )

        # Save the dashboard configuration
        import asyncio

        await asyncio.sleep(0.5)

        dashboard = dashboards.get("muslim-assistant")
        if dashboard and hasattr(dashboard, "async_save"):
            from .dashboard import DASHBOARD_CONFIG

            await dashboard.async_save(DASHBOARD_CONFIG)
            _LOGGER.info(
                "Muslim Assistant dashboard created automatically. "
                "Check the sidebar for the new dashboard."
            )
        else:
            _LOGGER.info(
                "Muslim Assistant dashboard registered in sidebar. "
                "You can customize it from Settings > Dashboards."
            )

    except Exception as err:
        _LOGGER.debug(
            "Could not auto-create dashboard (add manually via Settings > Dashboards): %s",
            err,
        )


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
