import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------------------------------------
# Konfiguration & Laden
# ---------------------------------------------------------
file_path = "data/full_data_transformed.csv"
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

# Plot: Boxplot pro Stunde (1.7.0)
plt.figure()
sns.boxplot(x="hour", y=value_col, data=df)
plt.title("Verbrauchsverteilung pro Stunde (1.7.0)")
plt.xlabel("Stunde")
plt.ylabel("Verbrauch (Watt)")
plt.tight_layout()
plt.savefig("visualize/plot_boxplot_by_hour.png")

# Plot: Histogramm mit 100 Bins (1.7.0)
plt.figure()
df[value_col].hist(bins=100)
plt.title("Histogramm des Stromverbrauchs (1.7.0, 100 Bins)")
plt.xlabel("Verbrauch (Watt)")
plt.ylabel("Häufigkeit")
plt.tight_layout()
plt.savefig("visualize/plot_histogram_100_bins.png")

# Plot: Scatterplot (Stunde vs Verbrauch)
plt.figure(figsize=(10, 5))
plt.scatter(df["hour"], df[value_col], alpha=0.1)
plt.title("Scatterplot: Verbrauch vs. Uhrzeit (1.7.0)")
plt.xlabel("Stunde")
plt.ylabel("Verbrauch (Watt)")
plt.tight_layout()
plt.savefig("visualize/plot_scatter_hour_vs_value.png")

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
pivot_heatmap_18 = df.pivot_table(index="weekday", columns="hour", values="verbrauch_interval", aggfunc="mean")
pivot_heatmap_18 = pivot_heatmap_18.reindex(weekday_order)

# Plot: Täglicher Durchschnitt aus 1.8.0
plt.figure()
plt.plot(daily_data_18["date"], daily_data_18["mean"])
plt.title("Täglicher Durchschnittsverbrauch aus 1.8.0 (kumuliert)")
plt.xlabel("Datum")
plt.ylabel("Durchschnittlicher Verbrauch (Wh)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualize/plot_daily_average_1_8.png")

# Plot: Balken nach Wochentag (1.8.0)
plt.figure()
sns.barplot(x="weekday", y="verbrauch_interval", data=weekday_data_18)
plt.title("Durchschnittlicher Verbrauch pro Wochentag (aus 1.8.0)")
plt.xlabel("Wochentag")
plt.ylabel("Verbrauch (Wh)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visualize/plot_avg_by_weekday_1_8.png")

# Plot: Heatmap (Stunde x Wochentag)
plt.figure(figsize=(12, 6))
sns.heatmap(pivot_heatmap_18, cmap="YlGnBu")
plt.title("Heatmap: Verbrauch je Stunde & Wochentag (aus 1.8.0)")
plt.xlabel("Stunde")
plt.ylabel("Wochentag")
plt.tight_layout()
plt.savefig("visualize/plot_heatmap_weekday_hour_1_8.png")

print("[INFO] Alle Diagramme wurden erfolgreich generiert und gespeichert.")
