"""
model_planning/hypothesis_test_full.py

Dieses Skript prüft die Hypothese:
- Tagsüber ist der Momentanverbrauch signifikant höher als nachts.
Es verwendet dazu den Mann-Whitney-U-Test (nichtparametrisch).
Zusätzlich werden Mittelwerte und Mediane berechnet.
"""

import pandas as pd
import os
from scipy.stats import mannwhitneyu

INPUT_CSV_PATH = os.path.join('data', 'full_data_transformed.csv')

print("[INFO] Lade transformierte CSV-Datei...")
df = pd.read_csv(INPUT_CSV_PATH, parse_dates=['timestamp'])

if '1.7.0' not in df.columns or 'day_night' not in df.columns:
    raise ValueError("Fehler: Benötigte Spalten (1.7.0 und day_night) fehlen in der CSV-Datei.")

# -------------------------------
# 3. Daten filtern
# -------------------------------
tag_data = df[df['day_night'] == 'Tag']['1.7.0'].dropna()
nacht_data = df[df['day_night'] == 'Nacht']['1.7.0'].dropna()

print(f"[INFO] Anzahl Tag-Daten: {len(tag_data)}")
print(f"[INFO] Anzahl Nacht-Daten: {len(nacht_data)}")

# -------------------------------
# 4. Mittelwerte und Mediane berechnen
# -------------------------------
tag_mean = tag_data.mean()
nacht_mean = nacht_data.mean()
tag_median = tag_data.median()
nacht_median = nacht_data.median()

print("\n=== Deskriptive Statistik ===")
print(f"Tag - Mittelwert: {tag_mean:.2f} Watt")
print(f"Nacht - Mittelwert: {nacht_mean:.2f} Watt")
print(f"Tag - Median: {tag_median:.2f} Watt")
print(f"Nacht - Median: {nacht_median:.2f} Watt")

# -------------------------------
# 5. Hypothesentest
# -------------------------------
print("\n[INFO] Führe Mann-Whitney-U-Test durch...")

statistic, p_value = mannwhitneyu(tag_data, nacht_data, alternative='greater')

print("\n=== Mann-Whitney-U-Test ===")
print(f"Teststatistik: {statistic:.2f}")
print(f"p-Wert: {p_value:.70f}")
print("[INFO] Hypothesentest abgeschlossen.")
