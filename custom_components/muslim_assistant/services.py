"""Services for Muslim Assistant integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_GET_SURAH = "get_surah"
SERVICE_GET_AYAH = "get_ayah"
SERVICE_TASBIH_INCREMENT = "tasbih_increment"
SERVICE_TASBIH_RESET = "tasbih_reset"
SERVICE_TASBIH_SET_TARGET = "tasbih_set_target"
SERVICE_TASBIH_SET_DHIKR = "tasbih_set_dhikr"
SERVICE_GET_DUA = "get_dua"

SCHEMA_GET_SURAH = vol.Schema(
    {
        vol.Required("surah_number"): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=114)
        ),
    }
)

SCHEMA_GET_AYAH = vol.Schema(
    {
        vol.Required("surah_number"): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=114)
        ),
        vol.Required("ayah_number"): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=286)
        ),
    }
)

SCHEMA_TASBIH_INCREMENT = vol.Schema(
    {
        vol.Optional("amount", default=1): vol.All(
            vol.Coerce(int), vol.Range(min=1)
        ),
    }
)

SCHEMA_TASBIH_SET_TARGET = vol.Schema(
    {
        vol.Required("target"): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=10000)
        ),
    }
)

SCHEMA_TASBIH_SET_DHIKR = vol.Schema(
    {
        vol.Required("dhikr"): str,
    }
)

SCHEMA_GET_DUA = vol.Schema(
    {
        vol.Optional("category"): str,
    }
)


async def async_register_services(hass: HomeAssistant) -> None:
    """Register Muslim Assistant services."""

    async def handle_get_surah(call: ServiceCall) -> dict[str, Any]:
        """Handle get_surah service call."""
        surah_number = call.data["surah_number"]

        for entry_id, coordinator in hass.data.get(DOMAIN, {}).items():
            result = await coordinator.async_get_surah(surah_number)
            if result:
                # Fire an event with the surah data
                hass.bus.async_fire(
                    f"{DOMAIN}_surah",
                    {
                        "surah_number": surah_number,
                        "data": result,
                    },
                )
                return result
        return {}

    async def handle_get_ayah(call: ServiceCall) -> dict[str, Any]:
        """Handle get_ayah service call."""
        surah_number = call.data["surah_number"]
        ayah_number = call.data["ayah_number"]

        for entry_id, coordinator in hass.data.get(DOMAIN, {}).items():
            result = await coordinator.async_get_ayah(surah_number, ayah_number)
            if result:
                hass.bus.async_fire(
                    f"{DOMAIN}_ayah",
                    {
                        "surah_number": surah_number,
                        "ayah_number": ayah_number,
                        "data": result,
                    },
                )
                return result
        return {}

    async def handle_tasbih_increment(call: ServiceCall) -> None:
        """Handle tasbih_increment service call."""
        amount = call.data.get("amount", 1)
        entity_reg = er.async_get(hass)

        for entry_id in hass.data.get(DOMAIN, {}):
            entity_id = entity_reg.async_get_entity_id(
                "sensor", DOMAIN, f"{entry_id}_tasbih"
            )
            if entity_id:
                state = hass.states.get(entity_id)
                if state:
                    entity = hass.data["entity_components"]["sensor"].get_entity(
                        entity_id
                    )
                    if entity and hasattr(entity, "increment"):
                        entity.increment(amount)

    async def handle_tasbih_reset(call: ServiceCall) -> None:
        """Handle tasbih_reset service call."""
        entity_reg = er.async_get(hass)

        for entry_id in hass.data.get(DOMAIN, {}):
            entity_id = entity_reg.async_get_entity_id(
                "sensor", DOMAIN, f"{entry_id}_tasbih"
            )
            if entity_id:
                entity = hass.data["entity_components"]["sensor"].get_entity(
                    entity_id
                )
                if entity and hasattr(entity, "reset"):
                    entity.reset()

    async def handle_tasbih_set_target(call: ServiceCall) -> None:
        """Handle tasbih_set_target service call."""
        target = call.data["target"]
        entity_reg = er.async_get(hass)

        for entry_id in hass.data.get(DOMAIN, {}):
            entity_id = entity_reg.async_get_entity_id(
                "sensor", DOMAIN, f"{entry_id}_tasbih"
            )
            if entity_id:
                entity = hass.data["entity_components"]["sensor"].get_entity(
                    entity_id
                )
                if entity and hasattr(entity, "set_target"):
                    entity.set_target(target)

    async def handle_tasbih_set_dhikr(call: ServiceCall) -> None:
        """Handle tasbih_set_dhikr service call."""
        dhikr = call.data["dhikr"]
        entity_reg = er.async_get(hass)

        for entry_id in hass.data.get(DOMAIN, {}):
            entity_id = entity_reg.async_get_entity_id(
                "sensor", DOMAIN, f"{entry_id}_tasbih"
            )
            if entity_id:
                entity = hass.data["entity_components"]["sensor"].get_entity(
                    entity_id
                )
                if entity and hasattr(entity, "set_dhikr"):
                    entity.set_dhikr(dhikr)

    async def handle_get_dua(call: ServiceCall) -> None:
        """Handle get_dua service call."""
        from .const import DAILY_DUAS

        category = call.data.get("category")

        if category:
            duas = [d for d in DAILY_DUAS if category.lower() in d["name"].lower()]
        else:
            duas = DAILY_DUAS

        hass.bus.async_fire(
            f"{DOMAIN}_duas",
            {"duas": duas},
        )

    # Register all services
    if not hass.services.has_service(DOMAIN, SERVICE_GET_SURAH):
        hass.services.async_register(
            DOMAIN, SERVICE_GET_SURAH, handle_get_surah, schema=SCHEMA_GET_SURAH
        )

    if not hass.services.has_service(DOMAIN, SERVICE_GET_AYAH):
        hass.services.async_register(
            DOMAIN, SERVICE_GET_AYAH, handle_get_ayah, schema=SCHEMA_GET_AYAH
        )

    if not hass.services.has_service(DOMAIN, SERVICE_TASBIH_INCREMENT):
        hass.services.async_register(
            DOMAIN,
            SERVICE_TASBIH_INCREMENT,
            handle_tasbih_increment,
            schema=SCHEMA_TASBIH_INCREMENT,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_TASBIH_RESET):
        hass.services.async_register(
            DOMAIN, SERVICE_TASBIH_RESET, handle_tasbih_reset
        )

    if not hass.services.has_service(DOMAIN, SERVICE_TASBIH_SET_TARGET):
        hass.services.async_register(
            DOMAIN,
            SERVICE_TASBIH_SET_TARGET,
            handle_tasbih_set_target,
            schema=SCHEMA_TASBIH_SET_TARGET,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_TASBIH_SET_DHIKR):
        hass.services.async_register(
            DOMAIN,
            SERVICE_TASBIH_SET_DHIKR,
            handle_tasbih_set_dhikr,
            schema=SCHEMA_TASBIH_SET_DHIKR,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_GET_DUA):
        hass.services.async_register(
            DOMAIN, SERVICE_GET_DUA, handle_get_dua, schema=SCHEMA_GET_DUA
        )
