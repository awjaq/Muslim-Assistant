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
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    ADHAN_SOUNDS,
    CALC_METHOD_MAP,
    CONF_ADHAN_SOUND,
    CONF_ASR_OFFSET,
    CONF_AUTO_ADHAN,
    CONF_AUTO_KAHF_FRIDAY,
    CONF_AUTO_NOTIFY,
    CONF_AUTO_QURAN_FAJR,
    CONF_AUTO_SUHOOR,
    CONF_CALC_METHOD,
    CONF_DHUHR_OFFSET,
    CONF_FAJR_OFFSET,
    CONF_ISHA_OFFSET,
    CONF_MAGHRIB_OFFSET,
    CONF_NOTIFY_SERVICE,
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
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            lat = self.hass.config.latitude
            lon = self.hass.config.longitude

            await self.async_set_unique_id(f"{lat}_{lon}")
            self._abort_if_unique_id_configured()

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
            menu_options=["audio", "prayer_adjustments", "automations"],
        )

    async def async_step_audio(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle audio/reciter options with device picker."""
        if user_input is not None:
            # Ensure target_media_player is always a list
            target = user_input.get(CONF_TARGET_PLAYER, [])
            if isinstance(target, str):
                target = [target] if target else []
            user_input[CONF_TARGET_PLAYER] = target

            new_options = {**self.options, **user_input}
            return self.async_create_entry(title="", data=new_options)

        # Get current targets (handle old single-string format)
        current_targets = self.options.get(CONF_TARGET_PLAYER, [])
        if isinstance(current_targets, str):
            current_targets = [current_targets] if current_targets else []

        return self.async_show_form(
            step_id="audio",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_QURAN_RECITER,
                        default=self.options.get(
                            CONF_QURAN_RECITER, DEFAULT_RECITER
                        ),
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=list(QURAN_RECITERS.keys()),
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Optional(
                        CONF_ADHAN_SOUND,
                        default=self.options.get(
                            CONF_ADHAN_SOUND, DEFAULT_ADHAN
                        ),
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=list(ADHAN_SOUNDS.keys()),
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Optional(
                        CONF_TARGET_PLAYER,
                        default=current_targets,
                    ): EntitySelector(
                        EntitySelectorConfig(
                            domain="media_player",
                            multiple=True,
                        )
                    ),
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

    async def async_step_automations(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle automation toggle options."""
        if user_input is not None:
            new_options = {**self.options, **user_input}
            return self.async_create_entry(title="", data=new_options)

        # Discover available notification services
        notify_services = [""]
        for service in self.hass.services.async_services().get(
            "notify", {}
        ):
            notify_services.append(f"notify.{service}")

        return self.async_show_form(
            step_id="automations",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_AUTO_ADHAN,
                        default=self.options.get(CONF_AUTO_ADHAN, False),
                    ): bool,
                    vol.Optional(
                        CONF_AUTO_NOTIFY,
                        default=self.options.get(CONF_AUTO_NOTIFY, False),
                    ): bool,
                    vol.Optional(
                        CONF_NOTIFY_SERVICE,
                        default=self.options.get(CONF_NOTIFY_SERVICE, ""),
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=notify_services,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Optional(
                        CONF_AUTO_QURAN_FAJR,
                        default=self.options.get(
                            CONF_AUTO_QURAN_FAJR, False
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_AUTO_KAHF_FRIDAY,
                        default=self.options.get(
                            CONF_AUTO_KAHF_FRIDAY, False
                        ),
                    ): bool,
                    vol.Optional(
                        CONF_AUTO_SUHOOR,
                        default=self.options.get(CONF_AUTO_SUHOOR, False),
                    ): bool,
                }
            ),
        )
