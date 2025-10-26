# Energieverbrauch

Ein Home Assistant Add-on zur Erfassung und Analyse von Verbrauchsdaten (Strom, Gas, Wasser etc.) mit Datum und Einheit.

## Funktionen
- Eingabe von Verbrauchswerten mit Datum
- Automatische Sensorerstellung
- Speicherung in Recorder oder SQLite
- Berechnung von Tages-, Wochen-, Monatsverbrauch
- Prognosefunktion

## Installation
1. Über HACS installieren oder manuell in `custom_components` einfügen
2. Ressourcen, Einheit und Speicherort auswählen
3. SQLite-Add-on wird empfohlen (z. B. SQLite Web)

## Beispielkonfiguration
```yaml
energieverbrauch:
  ressourcen:
    - name: Strom
      einheit: kWh
    - name: Aquarium
      einheit: L
  speicherort: sqlite
