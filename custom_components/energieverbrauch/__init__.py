from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow
from .const import DOMAIN
from .coordinator import init_db

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    if entry.data.get("speicherort") == "sqlite":
        success = init_db(hass)
        if not success:
            hass.components.persistent_notification.create(
                "Die SQLite-Datenbank konnte nicht geöffnet oder erstellt werden. Bitte prüfe, ob das SQLite Add-on installiert ist.",
                title="Energieverbrauch Integration",
                notification_id="energieverbrauch_sqlite_error"
            )

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
