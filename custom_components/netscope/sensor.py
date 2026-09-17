"""Sensor platform for NetScope network scanner."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo, CONNECTION_NETWORK_MAC

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up NetScope sensor entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    tracked_devices = set()

    @callback
    def _handle_coordinator_update() -> None:
        new_entities = []
        for device_id, data in coordinator.data.items():
            if device_id not in tracked_devices:
                tracked_devices.add(device_id)
                new_entities.append(NetScopeDeviceSensor(coordinator, device_id))
        if new_entities:
            async_add_entities(new_entities)

    coordinator.async_add_listener(_handle_coordinator_update)
    _handle_coordinator_update()

class NetScopeDeviceSensor(CoordinatorEntity, SensorEntity):
    """Representation of a discovered local network device."""

    def __init__(self, coordinator, device_id: str) -> None:
        super().__init__(coordinator)
        self._device_id = device_id

    @property
    def device_info(self) -> DeviceInfo:
        """Register the device inside Home Assistant's Device Registry."""
        data = self.coordinator.data.get(self._device_id, {})
        mac = data.get("mac")
        hostname = data.get("hostname", "Unknown Device")
        vendor = data.get("vendor", "Unknown")

        connections = {(CONNECTION_NETWORK_MAC, mac)} if mac else set()

        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=hostname,
            manufacturer=vendor if vendor != "Unknown" else None,
            connections=connections,
        )

    @property
    def name(self) -> str:
        data = self.coordinator.data.get(self._device_id, {})
        hostname = data.get("hostname", "Device")
        return f"{hostname} Status"

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{self._device_id}"

    @property
    def native_value(self) -> str:
        """Return the IP address as the sensor state."""
        data = self.coordinator.data.get(self._device_id, {})
        return data.get("ip", "Offline")

    @property
    def extra_state_attributes(self) -> dict:
        """Expose IP, MAC, Vendor, and Hostname as attributes."""
        return self.coordinator.data.get(self._device_id, {})
