"""Muslim Assistant - Home Assistant Integration.

A comprehensive Islamic companion integration providing prayer times,
Qibla direction, Hijri calendar, Quran verses, daily Duas, Ramadan
tracking, Adhan and Quran audio playback, and more.
"""

from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_LATITUDE,
    CONF_LONGITUDE,
    EVENT_HOMEASSISTANT_STARTED,
)
from homeassistant.core import Event, HomeAssistant

from .const import (
    CONF_AUTO_ADHAN,
    CONF_AUTO_KAHF_FRIDAY,
    CONF_AUTO_NOTIFY,
    CONF_AUTO_QURAN_FAJR,
    CONF_AUTO_SUHOOR,
    CONF_CALC_METHOD,
    CONF_NOTIFY_SERVICE,
    CONF_SCHOOL,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import MuslimAssistantCoordinator

_LOGGER = logging.getLogger(__name__)

NEXT_PRAYER_ENTITY = "sensor.muslim_assistant_next_prayer"
RAMADAN_ENTITY = "sensor.muslim_assistant_ramadan_tracker"


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

    # Set up internal automations based on user options
    _async_setup_automations(hass, entry)

    # Listen for options updates to reload coordinator
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    # Auto-create dashboard (after HA is fully started)
    async def _on_started(event: Event) -> None:
        await _async_create_dashboard(hass)

    if hass.is_running:
        await _async_create_dashboard(hass)
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _on_started)

    return True


def _async_setup_automations(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Set up internal automations based on user options.

    These run inside the integration -- no external automations.yaml needed.
    The user enables them from Configure > Automations.
    On options change, the integration reloads and re-registers listeners.
    """
    options = entry.options

    # ── Auto-play Adhan at every prayer time ──
    if options.get(CONF_AUTO_ADHAN, False):

        async def _handle_adhan_on_prayer(event: Event) -> None:
            """Play Adhan when the next prayer changes."""
            if event.data.get("entity_id") != NEXT_PRAYER_ENTITY:
                return
            old_state = event.data.get("old_state")
            new_state = event.data.get("new_state")
            if (
                old_state
                and new_state
                and old_state.state != new_state.state
                and new_state.state not in ("unknown", "unavailable")
                and new_state.state != "Sunrise"
            ):
                _LOGGER.info("Auto-playing Adhan for %s", new_state.state)
                await hass.services.async_call(
                    DOMAIN, "play_adhan", blocking=False
                )

        unsub = hass.bus.async_listen("state_changed", _handle_adhan_on_prayer)
        entry.async_on_unload(unsub)
        _LOGGER.debug("Automation enabled: auto-play Adhan at prayer times")

    # ── Prayer time mobile notification ──
    if options.get(CONF_AUTO_NOTIFY, False):
        notify_service = options.get(CONF_NOTIFY_SERVICE, "")

        if notify_service:

            async def _handle_prayer_notification(event: Event) -> None:
                """Send notification when prayer time arrives."""
                if event.data.get("entity_id") != NEXT_PRAYER_ENTITY:
                    return
                old_state = event.data.get("old_state")
                new_state = event.data.get("new_state")
                if (
                    old_state
                    and new_state
                    and old_state.state != new_state.state
                    and new_state.state not in ("unknown", "unavailable")
                ):
                    prayer_name = new_state.state
                    prayer_time = new_state.attributes.get("time", "")
                    service_parts = notify_service.split(".", 1)
                    if len(service_parts) == 2:
                        await hass.services.async_call(
                            service_parts[0],
                            service_parts[1],
                            {
                                "title": f"Prayer Time: {prayer_name}",
                                "message": (
                                    f"It's time for {prayer_name} prayer"
                                    f" at {prayer_time}"
                                ),
                            },
                            blocking=False,
                        )

            unsub = hass.bus.async_listen(
                "state_changed", _handle_prayer_notification
            )
            entry.async_on_unload(unsub)
            _LOGGER.debug(
                "Automation enabled: prayer notifications via %s",
                notify_service,
            )

    # ── Play Quran after Fajr ──
    if options.get(CONF_AUTO_QURAN_FAJR, False):
        _fajr_played_today: set[str] = set()

        async def _handle_quran_after_fajr(event: Event) -> None:
            """Play Surah Al-Mulk 15 minutes after Fajr."""
            if event.data.get("entity_id") != NEXT_PRAYER_ENTITY:
                return
            old_state = event.data.get("old_state")
            new_state = event.data.get("new_state")
            if (
                old_state
                and new_state
                and old_state.state == "Fajr"
                and new_state.state != "Fajr"
            ):
                today = datetime.now().strftime("%Y-%m-%d")
                if today in _fajr_played_today:
                    return
                _fajr_played_today.add(today)
                # Clean old dates
                _fajr_played_today.discard(
                    (datetime.now().replace(day=datetime.now().day - 1)).strftime(
                        "%Y-%m-%d"
                    )
                )
                _LOGGER.info("Auto-playing Quran after Fajr (Surah Al-Mulk)")
                import asyncio

                await asyncio.sleep(900)  # 15 minutes
                await hass.services.async_call(
                    DOMAIN,
                    "play_quran",
                    {"surah_number": 67},
                    blocking=False,
                )

        unsub = hass.bus.async_listen(
            "state_changed", _handle_quran_after_fajr
        )
        entry.async_on_unload(unsub)
        _LOGGER.debug("Automation enabled: Quran after Fajr")

    # ── Surah Al-Kahf on Friday ──
    if options.get(CONF_AUTO_KAHF_FRIDAY, False):
        _kahf_played_today: set[str] = set()

        async def _handle_kahf_friday(event: Event) -> None:
            """Play Surah Al-Kahf on Friday mornings."""
            if event.data.get("entity_id") != NEXT_PRAYER_ENTITY:
                return
            now = datetime.now()
            if now.weekday() != 4:  # Friday = 4
                return
            today = now.strftime("%Y-%m-%d")
            if today in _kahf_played_today:
                return
            new_state = event.data.get("new_state")
            if new_state and new_state.state == "Dhuhr":
                _kahf_played_today.add(today)
                _LOGGER.info("Auto-playing Surah Al-Kahf (Friday)")
                await hass.services.async_call(
                    DOMAIN,
                    "play_quran",
                    {"surah_number": 18},
                    blocking=False,
                )

        unsub = hass.bus.async_listen(
            "state_changed", _handle_kahf_friday
        )
        entry.async_on_unload(unsub)
        _LOGGER.debug("Automation enabled: Surah Al-Kahf on Fridays")

    # ── Suhoor reminder during Ramadan ──
    if options.get(CONF_AUTO_SUHOOR, False):
        notify_service = options.get(CONF_NOTIFY_SERVICE, "")

        if notify_service:

            async def _handle_suhoor_reminder(event: Event) -> None:
                """Send Suhoor reminder when Fajr is the next prayer."""
                if event.data.get("entity_id") != NEXT_PRAYER_ENTITY:
                    return
                new_state = event.data.get("new_state")
                if not new_state or new_state.state != "Fajr":
                    return
                # Check if Ramadan
                ramadan_state = hass.states.get(RAMADAN_ENTITY)
                if (
                    not ramadan_state
                    or not ramadan_state.attributes.get("is_ramadan")
                ):
                    return
                fajr_time = new_state.attributes.get("time", "")
                service_parts = notify_service.split(".", 1)
                if len(service_parts) == 2:
                    await hass.services.async_call(
                        service_parts[0],
                        service_parts[1],
                        {
                            "title": "Suhoor Reminder",
                            "message": (
                                f"Time to prepare for Suhoor! "
                                f"Fasting begins at {fajr_time} (Fajr)."
                            ),
                        },
                        blocking=False,
                    )

            unsub = hass.bus.async_listen(
                "state_changed", _handle_suhoor_reminder
            )
            entry.async_on_unload(unsub)
            _LOGGER.debug("Automation enabled: Suhoor reminders during Ramadan")


async def _async_create_dashboard(hass: HomeAssistant) -> None:
    """Create the Muslim Assistant Lovelace dashboard automatically."""
    try:
        lovelace_data = hass.data.get("lovelace")
        if not lovelace_data:
            return

        dashboards = getattr(lovelace_data, "dashboards", None)
        if dashboards is None:
            return

        if "muslim-assistant" in dashboards:
            return

        collection = getattr(lovelace_data, "dashboards_collection", None)
        if collection is None:
            return

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

        import asyncio

        await asyncio.sleep(0.5)

        dashboard = dashboards.get("muslim-assistant")
        if dashboard and hasattr(dashboard, "async_save"):
            from .dashboard import DASHBOARD_CONFIG

            await dashboard.async_save(DASHBOARD_CONFIG)
            _LOGGER.info("Muslim Assistant dashboard created in sidebar")

    except Exception as err:
        _LOGGER.debug("Could not auto-create dashboard: %s", err)


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
