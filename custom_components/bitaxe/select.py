"""Select platform for the BitAxe integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ASIC_FREQUENCY,
    ASIC_VOLTAGE,
    DISPLAY_SLEEP_OPTIONS,
    DISPLAY_SLEEP_VALUE_TO_LABEL,
    DOMAIN,
)
from .entity import BitAxeEntity


@dataclass(frozen=True, kw_only=True)
class BitAxeSelectEntityDescription(SelectEntityDescription):
    """Describe a BitAxe select entity."""

    api_key: str


SELECT_DESCRIPTIONS: tuple[BitAxeSelectEntityDescription, ...] = (
    BitAxeSelectEntityDescription(
        key="frequency",
        name="Frequency",
        icon="mdi:sine-wave",
        api_key="frequency",
        options=[],
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeSelectEntityDescription(
        key="core_voltage",
        name="Core Voltage",
        icon="mdi:lightning-bolt",
        api_key="coreVoltage",
        options=[],
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeSelectEntityDescription(
        key="display_rotation",
        name="Display Rotation",
        icon="mdi:screen-rotation",
        api_key="rotation",
        options=["0", "90", "180", "270"],
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeSelectEntityDescription(
        key="display_sleep",
        name="Display Sleep",
        icon="mdi:monitor-off",
        api_key="displayTimeout",
        options=list(DISPLAY_SLEEP_OPTIONS.keys()),
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BitAxe select entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        BitAxeSelect(coordinator, description, entry)
        for description in SELECT_DESCRIPTIONS
    )


class BitAxeSelect(BitAxeEntity, SelectEntity):
    """Representation of a BitAxe select entity."""

    entity_description: BitAxeSelectEntityDescription

    def __init__(
        self,
        coordinator,
        description: BitAxeSelectEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

        # Set model-specific options for frequency and voltage
        if description.key == "frequency":
            model = (coordinator.data or {}).get("ASICModel", "")
            self._attr_options = ASIC_FREQUENCY.get(model, ASIC_FREQUENCY.get("BM1370", []))
        elif description.key == "core_voltage":
            model = (coordinator.data or {}).get("ASICModel", "")
            self._attr_options = ASIC_VOLTAGE.get(model, ASIC_VOLTAGE.get("BM1370", []))
        else:
            self._attr_options = list(description.options)

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self.entity_description.api_key)
        if value is None:
            return None
        if self.entity_description.key == "display_sleep":
            return DISPLAY_SLEEP_VALUE_TO_LABEL.get(int(value))
        return str(value)

    async def async_select_option(self, option: str) -> None:
        """Set the selected option via PATCH."""
        from . import patch_bitaxe_system

        if self.entity_description.key == "display_sleep":
            api_value = DISPLAY_SLEEP_OPTIONS[option]
        else:
            api_value = int(option)

        ip_address = self._entry.data["ip_address"]
        await patch_bitaxe_system(
            self.hass, ip_address, {self.entity_description.api_key: api_value}
        )
        await self.coordinator.async_request_refresh()
