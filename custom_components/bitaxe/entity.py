"""Base entity for the BitAxe integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN


class BitAxeEntity(CoordinatorEntity):
    """Base class for all BitAxe entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the base BitAxe entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._device_name = entry.data.get("device_name", "BitAxe Miner")

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._device_name,
            "manufacturer": "Open Source Hardware",
            "model": "BitAxe Miner",
        }
