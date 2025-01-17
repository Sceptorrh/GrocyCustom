"""Sensor platform for Grocy Tasks and Chores integration."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    entities = []
    
    # Add Tasks sensor
    entities.append(GrocyTasksSensor(coordinator))
    
    # Add Chores sensor
    entities.append(GrocyChoresSensor(coordinator))
    
    async_add_entities(entities)


class GrocyTasksSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Grocy Tasks sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_tasks"
        self._attr_name = "Grocy Tasks"

    @property
    def native_value(self) -> int:
        """Return the number of tasks."""
        return len(self.coordinator.data["tasks"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        return {
            "tasks": self.coordinator.data["tasks"],
        }


class GrocyChoresSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Grocy Chores sensor."""

    def __init__(self, coordinator: DataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_chores"
        self._attr_name = "Grocy Chores"

    @property
    def native_value(self) -> int:
        """Return the number of chores."""
        return len(self.coordinator.data["chores"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        return {
            "chores": self.coordinator.data["chores"],
        }
