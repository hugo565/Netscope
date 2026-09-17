"""Config flow for NetScope integration."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_SUBNET, DEFAULT_SUBNET

async function_validate_input(hass: HomeAssistant, data: dict) -> dict:
    """Validate the user input allows us to connect."""
    # Add any basic checks here if needed
    return {"title": f"NetScope ({data[CONF_SUBNET]})"}

class NetScopeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NetScope."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=f"NetScope ({user_input[CONF_SUBNET]})",
                data=user_input
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_SUBNET, default=DEFAULT_SUBNET): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
