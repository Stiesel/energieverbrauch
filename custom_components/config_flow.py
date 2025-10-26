from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class EnergieverbrauchConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            ressourcen = [
                {"name": r.strip(), "einheit": user_input["einheit"]}
                for r in user_input["ressourcen"].split(",")
            ]
            return self.async_create_entry(title="Energieverbrauch", data={
                "ressourcen": ressourcen,
                "speicherort": user_input["speicherort"]
            })

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("ressourcen"): str,
                vol.Required("einheit"): vol.In(["kWh", "m³", "L", "€", "kg", "°C"]),
                vol.Required("speicherort"): vol.In(["recorder", "sqlite"])
            })
        )
