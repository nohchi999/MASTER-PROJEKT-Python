# Umgebung wurde zurückgesetzt. Imports und Code erneut ausführen.
import pandas as pd
import matplotlib.pyplot as plt
import os

# Pfad zur transformierten Datei
csv_path = os.path.join("data", "full_data_transformed.csv")

# CSV laden
print("[INFO] Lade transformierte CSV-Datei...")
df = pd.read_csv(csv_path, parse_dates=["timestamp"])

# Tagespeaks berechnen
print("[INFO] Berechne Tages-Peaks (1.7.0)...")
df['date'] = df['timestamp'].dt.date
daily_peaks = df.groupby('date')['1.7.0'].max().reset_index()
daily_peaks.rename(columns={'1.7.0': 'daily_peak_watt'}, inplace=True)

# Deskriptive Statistik
print("[INFO] Berechne deskriptive Statistik...")
stats = daily_peaks['daily_peak_watt'].describe()

# Visualisierung
plt.figure(figsize=(12, 6))
plt.plot(daily_peaks['date'], daily_peaks['daily_peak_watt'], marker='o', linestyle='-')
plt.title('Tägliche Spitzenlast (1.7.0) in Watt')
plt.xlabel('Datum')
plt.ylabel('Peak (Watt)')
plt.xticks(rotation=45)
plt.tight_layout()

# Plot speichern
plot_path = os.path.join("visualize", "daily_peak_analysis.png")
plt.savefig(plot_path)
plt.close()

stats, plot_path
