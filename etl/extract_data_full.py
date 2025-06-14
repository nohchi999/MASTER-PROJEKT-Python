"""
etl/extract_data_full.py

Dieses Skript liest die JSON-Datei mit allen Smart-Meter-Daten ein,
wandelt sie in einen DataFrame um und speichert das Ergebnis als CSV
für die weitere Verarbeitung.

Schritt:
1. JSON laden
2. Daten aufbereiten
3. DataFrame erzeugen
4. Speichern als CSV
"""

import json
import pandas as pd
import os

# -------------------------------
# Konfiguration
# -------------------------------
JSON_FILE_PATH = os.path.join('mqtt_messages_2.json')
OUTPUT_CSV_PATH = os.path.join('data', 'full_data.csv')

# -------------------------------
# 1. JSON laden
# -------------------------------
print("[INFO] Lade JSON-Datei...")
with open(JSON_FILE_PATH, 'r') as f:
    data = json.load(f)

print(f"[INFO] Anzahl Datensätze: {len(data)}")

# -------------------------------
# 2. Daten aufbereiten
# -------------------------------
print("[INFO] Daten transformieren...")

records = []
for entry in data:
    timestamp = entry.get('time') or entry.get('timestamp')
    topic = entry.get('topic', '')
    message = entry.get('message', {})

    # Kombiniere alle Daten in einer Zeile
    row = {
        'timestamp': timestamp,
        'topic': topic
    }
    row.update(message)
    records.append(row)

print(f"[INFO] Anzahl transformierter Zeilen: {len(records)}")

# -------------------------------
# 3. DataFrame erzeugen
# -------------------------------
df = pd.DataFrame(records)

# Konvertiere Zeitstempel in datetime-Format
df['timestamp'] = pd.to_datetime(df['timestamp'])

print("[INFO] Beispielhafte Daten:")
print(df.head())

# -------------------------------
# 4. Speichern als CSV
# -------------------------------
df.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"[INFO] DataFrame gespeichert als: {OUTPUT_CSV_PATH}")

print("[INFO] Datenextraktion abgeschlossen.")
