import sqlite3
from .const import SQLITE_DB

def init_db():
    conn = sqlite3.connect(SQLITE_DB)
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

def insert_reading(resource, date, value, unit):
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (resource, date, value, unit) VALUES (?, ?, ?, ?)",
                   (resource, date, value, unit))
    conn.commit()
    conn.close()

def get_latest_value(resource_name):
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM readings WHERE resource = ? ORDER BY date DESC LIMIT 1", (resource_name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
