"""Config flow for Muslim Assistant integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlowWithConfigEntry,
)
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    ADHAN_SOUNDS,
    CALC_METHOD_MAP,
    CONF_ADHAN_SOUND,
    CONF_ASR_OFFSET,
    CONF_CALC_METHOD,
    CONF_DHUHR_OFFSET,
    CONF_FAJR_OFFSET,
    CONF_ISHA_OFFSET,
    CONF_MAGHRIB_OFFSET,
    CONF_QURAN_RECITER,
    CONF_SCHOOL,
    CONF_TARGET_PLAYER,
    DEFAULT_ADHAN,
    DEFAULT_CALC_METHOD,
    DEFAULT_RECITER,
    DEFAULT_SCHOOL,
    DOMAIN,
    QURAN_RECITERS,
    SCHOOLS,
)

_LOGGER = logging.getLogger(__name__)


class MuslimAssistantConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Muslim Assistant."""

    VERSION = 2

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> MuslimAssistantOptionsFlow:
        """Get the options flow for this handler."""
        return MuslimAssistantOptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step.

        Location is auto-detected from Home Assistant's configured
        location (Settings > System > General). No need for the user
        to enter latitude/longitude manually.
        """
        errors: dict[str, str] = {}

        if user_input is not None:
            # Use HA's location automatically
            lat = self.hass.config.latitude
            lon = self.hass.config.longitude

            await self.async_set_unique_id(f"{lat}_{lon}")
            self._abort_if_unique_id_configured()

            # Store HA location in entry data
            data = {
                **user_input,
                CONF_LATITUDE: lat,
                CONF_LONGITUDE: lon,
            }

            return self.async_create_entry(
                title=user_input.get(CONF_NAME, "Muslim Assistant"),
                data=data,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_NAME, default="Muslim Assistant"
                    ): str,
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


class MuslimAssistantOptionsFlow(OptionsFlowWithConfigEntry):
    """Handle Muslim Assistant options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options - main menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["audio", "prayer_adjustments"],
        )

    async def async_step_audio(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle audio/reciter options."""
        if user_input is not None:
            new_options = {**self.options, **user_input}
            return self.async_create_entry(title="", data=new_options)

        return self.async_show_form(
            step_id="audio",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_QURAN_RECITER,
                        default=self.options.get(
                            CONF_QURAN_RECITER, DEFAULT_RECITER
                        ),
                    ): vol.In(list(QURAN_RECITERS.keys())),
                    vol.Optional(
                        CONF_ADHAN_SOUND,
                        default=self.options.get(
                            CONF_ADHAN_SOUND, DEFAULT_ADHAN
                        ),
                    ): vol.In(list(ADHAN_SOUNDS.keys())),
                    vol.Optional(
                        CONF_TARGET_PLAYER,
                        default=self.options.get(CONF_TARGET_PLAYER, ""),
                    ): str,
                }
            ),
        )

    async def async_step_prayer_adjustments(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle prayer time adjustment options."""
        if user_input is not None:
            new_options = {**self.options, **user_input}
            return self.async_create_entry(title="", data=new_options)

        return self.async_show_form(
            step_id="prayer_adjustments",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_FAJR_OFFSET,
                        default=self.options.get(CONF_FAJR_OFFSET, 0),
                    ): vol.All(
                        vol.Coerce(int), vol.Range(min=-30, max=30)
                    ),
                    vol.Optional(
                        CONF_DHUHR_OFFSET,
                        default=self.options.get(CONF_DHUHR_OFFSET, 0),
                    ): vol.All(
                        vol.Coerce(int), vol.Range(min=-30, max=30)
                    ),
                    vol.Optional(
                        CONF_ASR_OFFSET,
                        default=self.options.get(CONF_ASR_OFFSET, 0),
                    ): vol.All(
                        vol.Coerce(int), vol.Range(min=-30, max=30)
                    ),
                    vol.Optional(
                        CONF_MAGHRIB_OFFSET,
                        default=self.options.get(CONF_MAGHRIB_OFFSET, 0),
                    ): vol.All(
                        vol.Coerce(int), vol.Range(min=-30, max=30)
                    ),
                    vol.Optional(
                        CONF_ISHA_OFFSET,
                        default=self.options.get(CONF_ISHA_OFFSET, 0),
                    ): vol.All(
                        vol.Coerce(int), vol.Range(min=-30, max=30)
                    ),
                }
            ),
        )
