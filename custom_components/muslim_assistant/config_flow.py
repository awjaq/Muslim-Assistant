"""Config flow for Muslim Assistant integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CALC_METHOD_MAP,
    CONF_CALC_METHOD,
    CONF_SCHOOL,
    DEFAULT_CALC_METHOD,
    DEFAULT_SCHOOL,
    DOMAIN,
    SCHOOLS,
)

_LOGGER = logging.getLogger(__name__)


class MuslimAssistantConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Muslim Assistant."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_LATITUDE]}_{user_input[CONF_LONGITUDE]}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, "Muslim Assistant"),
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_NAME, default="Muslim Assistant"
                    ): str,
                    vol.Required(
                        CONF_LATITUDE,
                        default=self.hass.config.latitude,
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_LONGITUDE,
                        default=self.hass.config.longitude,
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_CALC_METHOD,
                        default=DEFAULT_CALC_METHOD,
                    ): vol.In(list(CALC_METHOD_MAP.keys())),
                    vol.Required(
                        CONF_SCHOOL,
                        default=DEFAULT_SCHOOL,
                    ): vol.In(list(SCHOOLS.keys())),
                }
            ),
            errors=errors,
        )
