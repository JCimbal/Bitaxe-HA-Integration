"""Number platform for the BitAxe integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BitAxeEntity


@dataclass(frozen=True, kw_only=True)
class BitAxeNumberEntityDescription(NumberEntityDescription):
    """Describe a BitAxe number entity."""

    api_key: str


NUMBER_DESCRIPTIONS: tuple[BitAxeNumberEntityDescription, ...] = (
    BitAxeNumberEntityDescription(
        key="stratum_port",
        name="Stratum Port",
        icon="mdi:ethernet",
        api_key="stratumPort",
        native_min_value=1,
        native_max_value=65535,
        native_step=1,
        mode=NumberMode.BOX,
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeNumberEntityDescription(
        key="fallback_stratum_port",
        name="Fallback Stratum Port",
        icon="mdi:ethernet",
        api_key="fallbackStratumPort",
        native_min_value=1,
        native_max_value=65535,
        native_step=1,
        mode=NumberMode.BOX,
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeNumberEntityDescription(
        key="core_voltage",
        name="Core Voltage",
        icon="mdi:lightning-bolt",
        api_key="coreVoltage",
        native_min_value=1000,
        native_max_value=1500,
        native_step=10,
        native_unit_of_measurement="mV",
        mode=NumberMode.BOX,
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeNumberEntityDescription(
        key="frequency",
        name="ASIC Frequency",
        icon="mdi:sine-wave",
        api_key="frequency",
        native_min_value=100,
        native_max_value=800,
        native_step=25,
        native_unit_of_measurement="MHz",
        mode=NumberMode.BOX,
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeNumberEntityDescription(
        key="fan_speed_setting",
        name="Fan Speed Setting",
        icon="mdi:fan",
        api_key="fanspeed",
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement="%",
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeNumberEntityDescription(
        key="temp_target",
        name="Target Temperature",
        icon="mdi:thermometer",
        api_key="temptarget",
        native_min_value=30,
        native_max_value=90,
        native_step=1,
        native_unit_of_measurement="°C",
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeNumberEntityDescription(
        key="display_timeout",
        name="Display Timeout",
        icon="mdi:monitor",
        api_key="displayTimeout",
        native_min_value=-1,
        native_max_value=3600,
        native_step=1,
        native_unit_of_measurement="s",
        mode=NumberMode.BOX,
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeNumberEntityDescription(
        key="stats_frequency",
        name="Stats Logging Interval",
        icon="mdi:chart-line",
        api_key="statsFrequency",
        native_min_value=1,
        native_max_value=3600,
        native_step=1,
        native_unit_of_measurement="s",
        mode=NumberMode.BOX,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BitAxe number entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        BitAxeNumber(coordinator, description, entry)
        for description in NUMBER_DESCRIPTIONS
    )


class BitAxeNumber(BitAxeEntity, NumberEntity):
    """Representation of a BitAxe number entity."""

    entity_description: BitAxeNumberEntityDescription

    def __init__(
        self,
        coordinator,
        description: BitAxeNumberEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.api_key)

    async def async_set_native_value(self, value: float) -> None:
        """Set the value via PATCH."""
        from . import patch_bitaxe_system

        ip_address = self._entry.data["ip_address"]
        await patch_bitaxe_system(
            self.hass, ip_address, {self.entity_description.api_key: int(value)}
        )
        await self.coordinator.async_request_refresh()
