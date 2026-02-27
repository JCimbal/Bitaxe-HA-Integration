"""Button platform for the BitAxe integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import BitAxeEntity


@dataclass(frozen=True, kw_only=True)
class BitAxeButtonEntityDescription(ButtonEntityDescription):
    """Describe a BitAxe button entity."""

    endpoint: str


BUTTON_DESCRIPTIONS: tuple[BitAxeButtonEntityDescription, ...] = (
    BitAxeButtonEntityDescription(
        key="restart",
        name="Restart",
        icon="mdi:restart",
        endpoint="/api/system/restart",
    ),
    BitAxeButtonEntityDescription(
        key="identify",
        name="Identify",
        icon="mdi:lightbulb-on-outline",
        endpoint="/api/system/identify",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BitAxe buttons from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        BitAxeButton(coordinator, description, entry)
        for description in BUTTON_DESCRIPTIONS
    )


class BitAxeButton(BitAxeEntity, ButtonEntity):
    """Representation of a BitAxe button."""

    entity_description: BitAxeButtonEntityDescription

    def __init__(
        self,
        coordinator,
        description: BitAxeButtonEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    async def async_press(self) -> None:
        """Handle the button press."""
        from . import post_bitaxe_command

        ip_address = self._entry.data["ip_address"]
        await post_bitaxe_command(
            self.hass, ip_address, self.entity_description.endpoint
        )
        await self.coordinator.async_request_refresh()
