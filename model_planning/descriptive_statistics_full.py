import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as ticker

# -------------------------------
# Konfiguration
# -------------------------------
INPUT_CSV_PATH = os.path.join('data', 'full_data_transformed.csv')
OUTPUT_PLOT_DIR = os.path.join('visualize')
os.makedirs(OUTPUT_PLOT_DIR, exist_ok=True)

# -------------------------------
# 1. CSV laden
# -------------------------------
print("[INFO] Lade transformierte CSV-Datei...")
df = pd.read_csv(INPUT_CSV_PATH, parse_dates=['timestamp'])

# -------------------------------
# 2. Metriken definieren
# -------------------------------
metrics = ['1.7.0', '1.8.0']

# -------------------------------
# 3. Plot-Einstellungen
# -------------------------------
bins = 50  # Anzahl der Bins für Histogramm (verstellbar)
x_axis_limit_1_7_0 = 1000 # Für bessere Lesbarkeit

# -------------------------------
# 4. Plots erstellen
# -------------------------------
print("[INFO] Erstelle Plots und speichere sie als PNG...")

for metric in metrics:
    if metric in df.columns:
        plot_data = df[metric].dropna()

        # Optional: Achsenlimits (nur für 1.7.0)
        if metric == '1.7.0':
            plot_data = plot_data[plot_data < x_axis_limit_1_7_0]

        # Histogramm
        plt.figure(figsize=(10, 6))
        plt.hist(plot_data, bins=bins, color='skyblue', edgecolor='black')
        plt.title(f'Histogramm: {metric}')
        plt.xlabel(f'{metric} (Watt)')
        plt.ylabel('Anzahl Messwerte')
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x/1000)}k'))
        histogram_path = os.path.join(OUTPUT_PLOT_DIR, f'{metric}_histogram.png')
        plt.savefig(histogram_path)
        plt.close()
        print(f"[INFO] Histogramm für {metric} gespeichert als: {histogram_path}")

        # Boxplot
        plt.figure(figsize=(6, 8))
        plt.boxplot(plot_data, vert=True)
        plt.title(f'Boxplot: {metric}')
        plt.ylabel(f'{metric} (Watt)')
        boxplot_path = os.path.join(OUTPUT_PLOT_DIR, f'{metric}_boxplot.png')
        plt.savefig(boxplot_path)
        plt.close()
        print(f"[INFO] Boxplot für {metric} gespeichert als: {boxplot_path}")

print("[INFO] Plots erfolgreich erstellt.")
