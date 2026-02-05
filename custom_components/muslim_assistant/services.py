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
SERVICE_CALCULATE_ZAKAT = "calculate_zakat"
SERVICE_GET_HAJJ_GUIDE = "get_hajj_guide"
SERVICE_GET_UMRAH_GUIDE = "get_umrah_guide"
SERVICE_SEND_GREETING = "send_greeting"
SERVICE_PRAYER_REQUEST = "prayer_request"
SERVICE_GET_ALLAH_NAMES = "get_allah_names"

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

SCHEMA_CALCULATE_ZAKAT = vol.Schema(
    {
        vol.Required("savings"): vol.Coerce(float),
        vol.Optional("gold_value", default=0): vol.Coerce(float),
        vol.Optional("silver_value", default=0): vol.Coerce(float),
        vol.Optional("business_assets", default=0): vol.Coerce(float),
        vol.Optional("stocks_investments", default=0): vol.Coerce(float),
        vol.Optional("rental_income", default=0): vol.Coerce(float),
        vol.Optional("other_income", default=0): vol.Coerce(float),
        vol.Optional("debts", default=0): vol.Coerce(float),
        vol.Optional("currency", default="USD"): str,
    }
)

SCHEMA_SEND_GREETING = vol.Schema(
    {
        vol.Required("occasion"): str,
        vol.Optional("recipient_name"): str,
        vol.Optional("custom_message"): str,
    }
)

SCHEMA_PRAYER_REQUEST = vol.Schema(
    {
        vol.Required("prayer_text"): str,
        vol.Optional("requester_name", default="Anonymous"): str,
        vol.Optional("category", default="general"): str,
    }
)

SCHEMA_GET_ALLAH_NAMES = vol.Schema(
    {
        vol.Optional("number"): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=99)
        ),
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

    async def handle_calculate_zakat(call: ServiceCall) -> None:
        """Handle calculate_zakat service call."""
        from .const import ZAKAT_NISAB_GOLD_GRAMS, ZAKAT_RATE

        savings = call.data["savings"]
        gold_value = call.data.get("gold_value", 0)
        silver_value = call.data.get("silver_value", 0)
        business_assets = call.data.get("business_assets", 0)
        stocks = call.data.get("stocks_investments", 0)
        rental = call.data.get("rental_income", 0)
        other = call.data.get("other_income", 0)
        debts = call.data.get("debts", 0)
        currency = call.data.get("currency", "USD")

        total_assets = (
            savings + gold_value + silver_value + business_assets
            + stocks + rental + other
        )
        net_assets = total_assets - debts
        zakat_amount = max(0, net_assets * ZAKAT_RATE)

        hass.bus.async_fire(
            f"{DOMAIN}_zakat",
            {
                "total_assets": round(total_assets, 2),
                "debts": round(debts, 2),
                "net_assets": round(net_assets, 2),
                "zakat_rate": f"{ZAKAT_RATE * 100}%",
                "zakat_amount": round(zakat_amount, 2),
                "currency": currency,
                "breakdown": {
                    "savings": savings,
                    "gold_value": gold_value,
                    "silver_value": silver_value,
                    "business_assets": business_assets,
                    "stocks_investments": stocks,
                    "rental_income": rental,
                    "other_income": other,
                },
            },
        )

    async def handle_get_hajj_guide(call: ServiceCall) -> None:
        """Handle get_hajj_guide service call."""
        from .const import HAJJ_GUIDE

        hass.bus.async_fire(
            f"{DOMAIN}_hajj_guide",
            {"guide": HAJJ_GUIDE},
        )

    async def handle_get_umrah_guide(call: ServiceCall) -> None:
        """Handle get_umrah_guide service call."""
        from .const import UMRAH_GUIDE

        hass.bus.async_fire(
            f"{DOMAIN}_umrah_guide",
            {"guide": UMRAH_GUIDE},
        )

    async def handle_send_greeting(call: ServiceCall) -> None:
        """Handle send_greeting service call."""
        from .const import GREETING_TEMPLATES

        occasion = call.data["occasion"]
        recipient = call.data.get("recipient_name", "")
        custom_msg = call.data.get("custom_message", "")

        # Find matching template
        template = None
        for t in GREETING_TEMPLATES:
            if occasion.lower() in t["occasion"].lower():
                template = t
                break

        if not template:
            template = GREETING_TEMPLATES[-2]  # General template

        greeting_text = template["greeting"]
        if recipient:
            greeting_text = f"Dear {recipient}, {greeting_text}"
        if custom_msg:
            greeting_text += f" {custom_msg}"

        hass.bus.async_fire(
            f"{DOMAIN}_greeting",
            {
                "occasion": template["occasion"],
                "greeting": greeting_text,
                "arabic": template["arabic"],
                "recipient": recipient,
            },
        )

    async def handle_prayer_request(call: ServiceCall) -> None:
        """Handle prayer_request service call."""
        prayer_text = call.data["prayer_text"]
        requester = call.data.get("requester_name", "Anonymous")
        category = call.data.get("category", "general")

        from datetime import datetime as dt

        hass.bus.async_fire(
            f"{DOMAIN}_prayer_request",
            {
                "prayer_text": prayer_text,
                "requester_name": requester,
                "category": category,
                "timestamp": dt.now().isoformat(),
            },
        )

    async def handle_get_allah_names(call: ServiceCall) -> None:
        """Handle get_allah_names service call."""
        from .const import NAMES_OF_ALLAH

        number = call.data.get("number")

        if number:
            names = [n for n in NAMES_OF_ALLAH if n["number"] == number]
        else:
            names = NAMES_OF_ALLAH

        hass.bus.async_fire(
            f"{DOMAIN}_allah_names",
            {"names": names, "total": len(NAMES_OF_ALLAH)},
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

    if not hass.services.has_service(DOMAIN, SERVICE_CALCULATE_ZAKAT):
        hass.services.async_register(
            DOMAIN,
            SERVICE_CALCULATE_ZAKAT,
            handle_calculate_zakat,
            schema=SCHEMA_CALCULATE_ZAKAT,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_GET_HAJJ_GUIDE):
        hass.services.async_register(
            DOMAIN, SERVICE_GET_HAJJ_GUIDE, handle_get_hajj_guide
        )

    if not hass.services.has_service(DOMAIN, SERVICE_GET_UMRAH_GUIDE):
        hass.services.async_register(
            DOMAIN, SERVICE_GET_UMRAH_GUIDE, handle_get_umrah_guide
        )

    if not hass.services.has_service(DOMAIN, SERVICE_SEND_GREETING):
        hass.services.async_register(
            DOMAIN,
            SERVICE_SEND_GREETING,
            handle_send_greeting,
            schema=SCHEMA_SEND_GREETING,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_PRAYER_REQUEST):
        hass.services.async_register(
            DOMAIN,
            SERVICE_PRAYER_REQUEST,
            handle_prayer_request,
            schema=SCHEMA_PRAYER_REQUEST,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_GET_ALLAH_NAMES):
        hass.services.async_register(
            DOMAIN,
            SERVICE_GET_ALLAH_NAMES,
            handle_get_allah_names,
            schema=SCHEMA_GET_ALLAH_NAMES,
        )
