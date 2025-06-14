import pandas as pd
import os
from scipy.stats import mannwhitneyu

INPUT_CSV_PATH = os.path.join('data', 'full_data_transformed.csv')

print("[INFO] Lade transformierte CSV-Datei...")
df = pd.read_csv(INPUT_CSV_PATH, parse_dates=['timestamp'])

tag_data = df[df['day_night'] == 'Tag']['1.7.0'].dropna()
nacht_data = df[df['day_night'] == 'Nacht']['1.7.0'].dropna()

print(f"[INFO] Anzahl Tag-Daten: {len(tag_data)}")
print(f"[INFO] Anzahl Nacht-Daten: {len(nacht_data)}")

print("\n[INFO] Führe Mann-Whitney-U-Test (zweiseitig) durch...")
stat, p = mannwhitneyu(tag_data, nacht_data, alternative='two-sided')

print("\n=== Mann-Whitney-U-Test ===")
print(f"Teststatistik: {stat:.2f}")
print(f"p-Wert: {p:.10f}")
print("Ergebnis:", "Signifikanter Unterschied (p < 0.05)" if p < 0.05 else "Kein signifikanter Unterschied")
