from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from .coordinator import get_latest_value

async def async_setup_entry(hass, entry, async_add_entities):
    ressourcen = entry.data.get("ressourcen", [])
    sensoren = []
    for res in ressourcen:
        sensoren.append(EnergieSensor(res["name"], res["einheit"]))
    async_add_entities(sensoren)

class EnergieSensor(SensorEntity):
    def __init__(self, name, einheit):
        self._attr_name = f"{name} Verbrauch"
        self._attr_native_unit_of_measurement = einheit
        self._attr_unique_id = f"energieverbrauch_{name.lower()}"
        self._state = None

    @property
    def native_value(self):
        return self._state

    async def async_update(self):
        self._state = get_latest_value(self._attr_name)
