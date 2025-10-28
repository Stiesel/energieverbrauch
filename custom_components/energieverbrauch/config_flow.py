from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import voluptuous as vol
import os
from .const import DOMAIN, SQLITE_DB
from .coordinator import insert_reading

def sqlite_available(hass: HomeAssistant) -> bool:
    db_path = os.path.join(hass.config.path(), SQLITE_DB)
    return os.path.exists(os.path.dirname(db_path))

class EnergieverbrauchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            ressourcen_raw = user_input.get("ressourcen", "")
            einheit = user_input.get("einheit")
            speicherort = user_input.get("speicherort")

            if speicherort == "sqlite" and not sqlite_available(self.hass):
                errors["speicherort"] = "sqlite_nicht_verfuegbar"
            else:
                ressourcen = [
                    {"name": r.strip(), "einheit": einheit}
                    for r in ressourcen_raw.split(",")
                ]
                return self.async_create_entry(
                    title="Energieverbrauch",
                    data={
                        "ressourcen": ressourcen,
                        "speicherort": speicherort
                    }
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("ressourcen"): str,
                vol.Required("einheit"): vol.In(["kWh", "m³", "L", "€", "kg", "°C"]),
                vol.Required("speicherort"): vol.In(["recorder", "sqlite"])
            }),
            errors=errors
        )

    async def async_step_input(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                insert_reading(
                    resource=user_input["ressource"],
                    date=user_input["datum"],
                    value=float(user_input["wert"]),
                    unit=user_input["einheit"]
                )
                return self.async_abort(reason="eingabe_erfolgreich")
            except Exception as e:
                errors["base"] = "speicherfehler"

        return self.async_show_form(
            step_id="input",
            data_schema=vol.Schema({
                vol.Required("datum"): str,  # z. B. "2025-10-27"
                vol.Required("ressource"): str,
                vol.Required("wert"): float,
                vol.Required("einheit"): vol.In(["kWh", "m³", "L", "€", "kg", "°C"])
            }),
            errors=errors
        )
