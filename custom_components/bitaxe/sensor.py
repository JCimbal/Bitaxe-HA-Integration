"""Sensor platform for the BitAxe integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .entity import BitAxeEntity


def format_difficulty(value) -> str | None:
    """Convert difficulty values into human-readable units (k, M, G, T, P, E)."""
    if value is None:
        return None

    try:
        value = float(value)
    except (ValueError, TypeError):
        return str(value)

    units = [
        (1e18, "E"),
        (1e15, "P"),
        (1e12, "T"),
        (1e9, "G"),
        (1e6, "M"),
        (1e3, "k"),
    ]

    for factor, suffix in units:
        if value >= factor:
            return f"{value / factor:.2f} {suffix}"

    return str(int(value))


SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="power",
        name="Power Consumption",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
        suggested_display_precision=1,
    ),
    SensorEntityDescription(
        key="temp",
        name="Temperature ASIC",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="vrTemp",
        name="Temperature VR",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
    ),
    SensorEntityDescription(
        key="hashRate",
        name="Hash Rate",
        native_unit_of_measurement="GH/s",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:speedometer",
        suggested_display_precision=0,
    ),
    SensorEntityDescription(
        key="bestDiff",
        name="All-Time Best Difficulty",
        icon="mdi:trophy",
    ),
    SensorEntityDescription(
        key="bestSessionDiff",
        name="Best Difficulty Since System Boot",
        icon="mdi:star",
    ),
    SensorEntityDescription(
        key="sharesAccepted",
        name="Shares Accepted",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:share",
    ),
    SensorEntityDescription(
        key="sharesRejected",
        name="Shares Rejected",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:share-off",
    ),
    SensorEntityDescription(
        key="fanspeed",
        name="Fan Speed",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="fanrpm",
        name="Fan RPM",
        native_unit_of_measurement="RPM",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
    SensorEntityDescription(
        key="uptimeSeconds",
        name="Uptime",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        icon="mdi:clock",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BitAxe sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        BitAxeSensor(coordinator, description, entry)
        for description in SENSOR_DESCRIPTIONS
    )


class BitAxeSensor(BitAxeEntity, SensorEntity):
    """Representation of a BitAxe sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def native_value(self):
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get(self.entity_description.key)

        if self.entity_description.key in ("bestDiff", "bestSessionDiff"):
            return format_difficulty(value)

        return value
