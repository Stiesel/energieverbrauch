from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import init_db
import os

def sqlite_available(hass: HomeAssistant) -> bool:
    db_path = os.path.join(hass.config.path(), "energieverbrauch.db")
    return os.path.exists(os.path.dirname(db_path))

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    if entry.data.get("speicherort") == "sqlite":
        if not sqlite_available(hass):
            hass.components.persistent_notification.create(
                "SQLite wurde als Speicherort gewählt, aber scheint nicht installiert zu sein. "
                "Bitte installiere ein SQLite-Add-on oder wähle 'recorder'.",
                title="Energieverbrauch Integration",
                notification_id="energieverbrauch_sqlite_missing"
            )
            return False

        success = init_db(hass)
        if not success:
            hass.components.persistent_notification.create(
                "Die SQLite-Datenbank konnte nicht geöffnet oder erstellt werden. "
                "Bitte prüfe, ob das SQLite Add-on korrekt installiert ist.",
                title="Energieverbrauch Integration",
                notification_id="energieverbrauch_sqlite_error"
            )
            return False

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
