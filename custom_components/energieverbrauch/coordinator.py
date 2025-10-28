import os
import sqlite3
import logging
from homeassistant.core import HomeAssistant
from .const import SQLITE_DB

_LOGGER = logging.getLogger(__name__)

def init_db(hass: HomeAssistant) -> bool:
    """Initialisiert die SQLite-Datenbank, falls sie noch nicht existiert."""
    db_path = os.path.join(hass.config.path(), SQLITE_DB)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource TEXT NOT NULL,
                date TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()
        _LOGGER.info("SQLite-Datenbank initialisiert: %s", db_path)
        return True
    except Exception as e:
        _LOGGER.error("Fehler beim Initialisieren der SQLite-Datenbank: %s", e)
        return False

def insert_reading(resource: str, date: str, value: float, unit: str) -> bool:
    """Speichert einen neuen Verbrauchswert in der Datenbank."""
    try:
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO readings (resource, date, value, unit)
            VALUES (?, ?, ?, ?)
        """, (resource, date, value, unit))
        conn.commit()
        conn.close()
        _LOGGER.info("Neuer Verbrauchswert gespeichert: %s - %s %s am %s", resource, value, unit, date)
        return True
    except Exception as e:
        _LOGGER.error("Fehler beim Speichern des Verbrauchswerts: %s", e)
        return False

def get_latest_value(resource_name: str) -> float | None:
    """Liefert den zuletzt gespeicherten Wert für eine Ressource."""
    try:
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT value FROM readings
            WHERE resource = ?
            ORDER BY date DESC
            LIMIT 1
        """, (resource_name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            _LOGGER.debug("Letzter Wert für %s: %s", resource_name, row[0])
            return row[0]
        else:
            _LOGGER.debug("Keine Werte für Ressource %s gefunden.", resource_name)
            return None
    except Exception as e:
        _LOGGER.warning("Fehler beim Abrufen des letzten Werts: %s", e)
        return None
