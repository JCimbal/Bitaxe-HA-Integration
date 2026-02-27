"""Switch platform for the BitAxe integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BitAxeEntity


@dataclass(frozen=True, kw_only=True)
class BitAxeSwitchEntityDescription(SwitchEntityDescription):
    """Describe a BitAxe switch entity."""

    api_key: str


SWITCH_DESCRIPTIONS: tuple[BitAxeSwitchEntityDescription, ...] = (
    BitAxeSwitchEntityDescription(
        key="use_fallback_stratum",
        name="Use Fallback Stratum",
        icon="mdi:server-network",
        api_key="useFallbackStratum",
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeSwitchEntityDescription(
        key="overclock_enabled",
        name="Overclock Enabled",
        icon="mdi:speedometer",
        api_key="overclockEnabled",
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeSwitchEntityDescription(
        key="auto_fan_speed",
        name="Auto Fan Speed",
        icon="mdi:fan-auto",
        api_key="autofanspeed",
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeSwitchEntityDescription(
        key="invert_screen",
        name="Invert Display",
        icon="mdi:monitor-eye",
        api_key="invertscreen",
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeSwitchEntityDescription(
        key="overheat_mode",
        name="Overheat Mode",
        icon="mdi:fire-alert",
        api_key="overheat_mode",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BitAxe switches from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        BitAxeSwitch(coordinator, description, entry)
        for description in SWITCH_DESCRIPTIONS
    )


class BitAxeSwitch(BitAxeEntity, SwitchEntity):
    """Representation of a BitAxe switch."""

    entity_description: BitAxeSwitchEntityDescription

    def __init__(
        self,
        coordinator,
        description: BitAxeSwitchEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self.entity_description.api_key)
        if value is None:
            return None
        return bool(value)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        await self._async_set_value(1)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        await self._async_set_value(0)

    async def _async_set_value(self, value: int) -> None:
        """Send the PATCH request and refresh."""
        from . import patch_bitaxe_system

        ip_address = self._entry.data["ip_address"]
        await patch_bitaxe_system(
            self.hass, ip_address, {self.entity_description.api_key: value}
        )
        await self.coordinator.async_request_refresh()
