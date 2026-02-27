"""Text platform for the BitAxe integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.text import TextEntity, TextEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BitAxeEntity


@dataclass(frozen=True, kw_only=True)
class BitAxeTextEntityDescription(TextEntityDescription):
    """Describe a BitAxe text entity."""

    api_key: str


TEXT_DESCRIPTIONS: tuple[BitAxeTextEntityDescription, ...] = (
    BitAxeTextEntityDescription(
        key="stratum_url",
        name="Stratum URL",
        icon="mdi:server-network",
        api_key="stratumURL",
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeTextEntityDescription(
        key="stratum_user",
        name="Stratum User",
        icon="mdi:account",
        api_key="stratumUser",
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeTextEntityDescription(
        key="fallback_stratum_url",
        name="Fallback Stratum URL",
        icon="mdi:server-network-off",
        api_key="fallbackStratumURL",
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeTextEntityDescription(
        key="fallback_stratum_user",
        name="Fallback Stratum User",
        icon="mdi:account-outline",
        api_key="fallbackStratumUser",
        entity_category=EntityCategory.CONFIG,
    ),
    BitAxeTextEntityDescription(
        key="hostname",
        name="Hostname",
        icon="mdi:label",
        api_key="hostname",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BitAxe text entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        BitAxeText(coordinator, description, entry)
        for description in TEXT_DESCRIPTIONS
    )


class BitAxeText(BitAxeEntity, TextEntity):
    """Representation of a BitAxe text entity."""

    entity_description: BitAxeTextEntityDescription

    def __init__(
        self,
        coordinator,
        description: BitAxeTextEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the text entity."""
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def native_value(self) -> str | None:
        """Return the current text value."""
        if self.coordinator.data is None:
            return None
        value = self.coordinator.data.get(self.entity_description.api_key)
        if value is None:
            return None
        return str(value)

    async def async_set_value(self, value: str) -> None:
        """Set the text value via PATCH."""
        from . import patch_bitaxe_system

        ip_address = self._entry.data["ip_address"]
        await patch_bitaxe_system(
            self.hass, ip_address, {self.entity_description.api_key: value}
        )
        await self.coordinator.async_request_refresh()
