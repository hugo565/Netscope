"""The NetScope integration setup."""

import logging
import shutil

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_SUBNET, DEFAULT_SUBNET
from .coordinator import NetScopeCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NetScope from a config entry."""
    
    # Ensure nmap is installed on the host system
    if not shutil.which("nmap"):
        _LOGGER.error("The 'nmap' utility is not installed on the host system. NetScope cannot run.")
        raise HomeAssistantError("Nmap executable not found on host. Please install nmap.")

    target_subnet = entry.data.get(CONF_SUBNET, DEFAULT_SUBNET)

    coordinator = NetScopeCoordinator(hass, target_subnet)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
