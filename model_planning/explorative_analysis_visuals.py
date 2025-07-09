import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------------------------------------
# Konfiguration & Laden
# ---------------------------------------------------------
file_path = os.path.join("data", "full_data_transformed.csv")
df = pd.read_csv(file_path, parse_dates=["timestamp"])

# ---------------------------------------------------------
# Vorbereitung
# ---------------------------------------------------------
df["hour"] = df["timestamp"].dt.hour
df["date"] = df["timestamp"].dt.date
df["weekday"] = df["timestamp"].dt.day_name()

# ---------------------------------------------------------
# Verbrauch aus 1.7.0 (Momentanverbrauch)
# ---------------------------------------------------------
value_col = "1.7.0"

# Boxplot pro Stunde
plt.figure()
sns.boxplot(x="hour", y=value_col, data=df)
plt.title("Verbrauchsverteilung pro Stunde (1.7.0)")
plt.xlabel("Stunde")
plt.ylabel("Verbrauch (Watt)")
plt.tight_layout()
plt.savefig(os.path.join("visualize", "plot_boxplot_by_hour.png"))
plt.close()

# Histogramm mit 100 Bins
plt.figure()
df[value_col].hist(bins=100)
plt.title("Histogramm des Stromverbrauchs (1.7.0, 100 Bins)")
plt.xlabel("Verbrauch (Watt)")
plt.ylabel("Häufigkeit")
plt.tight_layout()
plt.savefig(os.path.join("visualize", "plot_histogram_100_bins.png"))
plt.close()

# Scatterplot: Stunde vs Verbrauch
plt.figure(figsize=(10, 5))
plt.scatter(df["hour"], df[value_col], alpha=0.1)
plt.title("Scatterplot: Verbrauch vs. Uhrzeit (1.7.0)")
plt.xlabel("Stunde")
plt.ylabel("Verbrauch (Watt)")
plt.tight_layout()
plt.savefig(os.path.join("visualize", "plot_scatter_hour_vs_value.png"))
plt.close()

# ---------------------------------------------------------
# Verbrauch aus 1.8.0 (kumulativ → Verbrauch pro Intervall)
# ---------------------------------------------------------
df = df.sort_values("timestamp")
df["verbrauch_interval"] = df["1.8.0"].diff().fillna(0) * 1000  # kWh → Wh

# Tagesdaten

daily_data_18 = df.groupby("date")["verbrauch_interval"].agg(["mean", "max"]).reset_index()

# Wochentagsdaten
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_data_18 = df.groupby("weekday")["verbrauch_interval"].mean().reindex(weekday_order).reset_index()

# Heatmapdaten
pivot_heatmap_18 = df.pivot_table(index="weekday", columns="hour", values="verbrauch_interval", aggfunc="mean").reindex(weekday_order)

# Plot: Täglicher Durchschnitt aus 1.8.0\plt.figure()
plt.plot(daily_data_18["date"], daily_data_18["mean"] )
plt.title("Täglicher Durchschnittsverbrauch aus 1.8.0 (kumuliert)")
plt.xlabel("Datum")
plt.ylabel("Durchschnittlicher Verbrauch (Wh)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join("visualize", "plot_daily_average_1_8.png"))
plt.close()

# Plot: Balken nach Wochentag (1.8.0)
plt.figure()
sns.barplot(x="weekday", y="verbrauch_interval", data=weekday_data_18)
plt.title("Durchschnittlicher Verbrauch pro Wochentag (aus 1.8.0)")
plt.xlabel("Wochentag")
plt.ylabel("Verbrauch (Wh)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join("visualize", "plot_avg_by_weekday_1_8.png"))
plt.close()

# Plot: Heatmap (Stunde x Wochentag)
plt.figure(figsize=(12, 6))
sns.heatmap(pivot_heatmap_18, cmap="YlGnBu")
plt.title("Heatmap: Verbrauch je Stunde & Wochentag (aus 1.8.0)")
plt.xlabel("Stunde")
plt.ylabel("Wochentag")
plt.tight_layout()
plt.savefig(os.path.join("visualize", "plot_heatmap_weekday_hour_1_8.png"))
plt.close()

# ---------------------------------------------------------
# Tägliche Spitzenlast (1.7.0)
# ---------------------------------------------------------
# Kein Interpolieren: Direkte Max-Berechnung pro Tag
print("[INFO] Berechne Tages-Peaks (1.7.0) ohne Interpolation...")
daily_peaks = df.groupby('date')[value_col].max().reset_index()
daily_peaks.rename(columns={value_col: 'daily_peak_watt'}, inplace=True)

# Deskriptive Statistik der Tages-Peaks
print("[INFO] Berechne deskriptive Statistik der Tages-Peaks...")
stats = daily_peaks['daily_peak_watt'].describe()
print(stats)

# ---------------------------------------------------------
# Tägliche Spitzenlast (1.7.0)
# ---------------------------------------------------------
# Kein Interpolieren: Direkte Max-Berechnung pro Tag
print("[INFO] Berechne Tages-Peaks (1.7.0) ohne Interpolation...")
daily_peaks = df.groupby("date")[value_col].max().reset_index()
daily_peaks.rename(columns={value_col: "daily_peak_watt"}, inplace=True)

# Deskriptive Statistik der Tages-Peaks
print("[INFO] Berechne deskriptive Statistik der Tages-Peaks...")
stats = daily_peaks["daily_peak_watt"].describe()
print(stats)

# Visualisierung: Tägliche Spitzenlast ohne Linienverbindung
plt.figure(figsize=(12, 6))
plt.scatter(daily_peaks["date"], daily_peaks["daily_peak_watt"], marker='o')
plt.title("Tägliche Spitzenlast (1.7.0) in Watt")
plt.xlabel("Datum")
plt.ylabel("Peak (Watt)")
plt.xticks(rotation=45)
plt.tight_layout()
pd_visual = os.path.join("visualize", "daily_peak_analysis.png")
plt.savefig(pd_visual)
plt.close()

print("[INFO] Alle Diagramme wurden erfolgreich generiert und gespeichert.")
