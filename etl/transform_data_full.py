"""
etl/transform_data_full.py

Dieses Skript transformiert den DataFrame:
- Wandelt den Zeitstempel in ein datetime-Format
- Konvertiert wichtige Messwerte in numerische Typen
- Entfernt unwichtige Spalten (optional)
- Entfernt Duplikate
- Filtert Extremwerte
- Erstellt eine Tag/Nacht-Spalte
- Speichert den transformierten DataFrame als CSV
"""

import pandas as pd
import os


INPUT_CSV_PATH = os.path.join('data', 'full_data.csv')
OUTPUT_CSV_PATH = os.path.join('data', 'full_data_transformed.csv')


print("[INFO] Lade CSV-Datei...")
df = pd.read_csv(INPUT_CSV_PATH)

# -------------------------------
# 2. Zeitstempel konvertieren
# -------------------------------
print("[INFO] Konvertiere Zeitstempel...")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# -------------------------------
# 3. Wichtige Spalten in float umwandeln
# -------------------------------
print("[INFO] Konvertiere numerische Spalten...")

numerical_columns = [
    '1.7.0', '1.8.0', '2.7.0', '2.8.0', '3.8.0', '4.8.0', '16.7.0',
    '31.7.0', '32.7.0', '51.7.0', '52.7.0', '71.7.0', '72.7.0'
]

for col in numerical_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# -------------------------------
# 4. Unwichtige Spalten entfernen
# -------------------------------
print("[INFO] Entferne unwichtige Spalten...")
drop_columns = ['topic', 'uptime'] + [col for col in numerical_columns if col.startswith(('31.', '32.', '51.', '52.', '71.', '72.'))]
df.drop(columns=[col for col in drop_columns if col in df.columns], inplace=True)

print(f"[INFO] Verbleibende Spalten: {df.columns.tolist()}")
print(f"[INFO] Anzahl der Zeilen nach Spaltenfilter: {len(df)}")

# -------------------------------
# 5. Duplikate entfernen
# -------------------------------
print("[INFO] Entferne Duplikate...")
before = len(df)
df.drop_duplicates(inplace=True)
after = len(df)
print(f"[INFO] Anzahl der Zeilen nach Duplikat-Filter: {after}")


# -------------------------------
# 6. Extremwerte filtern
# -------------------------------
print("[INFO] Filtere Extremwerte...")
threshold_1_7_0 = 10000  # Plausibilitätsgrenze
if '1.7.0' in df.columns:
    before = len(df)
    df = df[df['1.7.0'] < threshold_1_7_0]
    after = len(df)
    print(f"[INFO] Anzahl der Zeilen nach Extremwertfilter (1.7.0 < {threshold_1_7_0}): {after}")

# -------------------------------
# 6.5. Nullwerte entfernen
# -------------------------------
print("[INFO] Entferne Zeilen mit 1.7.0 == 0...")
if '1.7.0' in df.columns:
    before = len(df)
    df = df[df['1.7.0'] > 0]
    after = len(df)
    print(f"[INFO] Anzahl der Zeilen nach 0-Filter (1.7.0 > 0): {after}")

# -------------------------------
# 7. Tag/Nacht-Spalte hinzufügen
# -------------------------------
print("[INFO] Erstelle Tag/Nacht-Spalte...")

def classify_day_night(hour):
    return 'Tag' if 6 <= hour < 21 else 'Nacht'

df['day_night'] = df['timestamp'].dt.hour.apply(classify_day_night)

# -------------------------------
# 8. Kontrolle & Speichern
# -------------------------------
print("[INFO] Beispielhafte Daten nach Transformation:")
print(df.head())

df.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"[INFO] Transformierte Daten gespeichert als: {OUTPUT_CSV_PATH}")

print("[INFO] Transformation abgeschlossen.")
