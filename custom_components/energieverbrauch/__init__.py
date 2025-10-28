from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import service
from .const import DOMAIN, SQLITE_DB
from .coordinator import init_db, insert_reading
import os

def sqlite_available(hass: HomeAssistant) -> bool:
    db_path = os.path.join(hass.config.path(), SQLITE_DB)
    return os.path.exists(os.path.dirname(db_path))

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    # Prüfen ob SQLite verfügbar ist
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
                "Die SQLite-Datenbank konnte nicht geöffnet oder erstellt werden.",
                title="Energieverbrauch Integration",
                notification_id="energieverbrauch_sqlite_error"
            )
            return False

    # Eingabefelder automatisch erstellen
    await hass.services.async_call("input_datetime", "create", {
        "name": "energieverbrauch_datum",
        "has_date": True,
        "has_time": False
    }, blocking=True)

    await hass.services.async_call("input_select", "create", {
        "name": "energieverbrauch_ressource",
        "options": [r["name"] for r in entry.data["ressourcen"]],
        "initial": entry.data["ressourcen"][0]["name"]
    }, blocking=True)

    await hass.services.async_call("input_number", "create", {
        "name": "energieverbrauch_wert",
        "min": 0,
        "max": 10000,
        "step": 0.1,
        "mode": "box"
    }, blocking=True)

    await hass.services.async_call("input_button", "create", {
        "name": "energieverbrauch_speichern"
    }, blocking=True)

    # Service zum Speichern registrieren
    async def handle_add_reading(call):
        resource = call.data.get("resource")
        date = call.data.get("date")
        value = call.data.get("value")
        unit = call.data.get("unit")
        success = insert_reading(resource, date, value, unit)
        if not success:
            hass.components.persistent_notification.create(
                f"Fehler beim Speichern des Verbrauchswerts für {resource}.",
                title="Energieverbrauch",
                notification_id="energieverbrauch_speicherfehler"
            )

    hass.services.async_register(DOMAIN, "add_reading", handle_add_reading)

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
