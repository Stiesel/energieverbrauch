import os
import sqlite3
import logging
from homeassistant.core import HomeAssistant
from .const import SQLITE_DB

_LOGGER = logging.getLogger(__name__)

def init_db(hass: HomeAssistant):
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

def get_latest_value(resource_name):
    try:
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM readings WHERE resource = ? ORDER BY date DESC LIMIT 1", (resource_name,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
    except Exception as e:
        _LOGGER.warning("SQLite-Abfrage fehlgeschlagen: %s", e)
        return None
