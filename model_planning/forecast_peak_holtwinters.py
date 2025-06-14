import pandas as pd
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# === KONFIGURATION ===
INPUT_CSV_PATH = os.path.join("data", "full_data_transformed.csv")
OUTPUT_PLOT_PATH = os.path.join("visualize", "holtwinters_forecast.png")

# === DATEN EINLESEN ===
print("[INFO] Lade CSV-Datei...")
df = pd.read_csv(INPUT_CSV_PATH, parse_dates=["timestamp"])
df = df[["timestamp", "1.7.0"]].dropna()
df.set_index("timestamp", inplace=True)

# === TÄGLICHES MAXIMUM BERECHNEN ===
print("[INFO] Aggregiere Tagesmaxima von 1.7.0...")
daily_max = df["1.7.0"].resample("D").max()

# === TRAIN-/TEST-SPLIT ===
train_size = int(len(daily_max) * 0.8)
train, test = daily_max[:train_size], daily_max[train_size:]

# === MODELL TRAINIEREN ===
print("[INFO] Trainiere Holt-Winters Modell...")
model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=7)
fit = model.fit()

# === PROGNOSE ERSTELLEN ===
forecast_days = len(test) + 1
forecast = fit.forecast(forecast_days)

# === PLOT ERSTELLEN ===
plt.figure(figsize=(12, 6))
plt.plot(train.index, train, label="Trainingsdaten")
plt.plot(test.index, test, label="Testdaten")
plt.plot(forecast.index, forecast, label="Vorhersage", linestyle="--")
plt.title("Täglicher Spitzenverbrauch – Holt-Winters Prognose")
plt.xlabel("Datum")
plt.ylabel("Maximale Leistung (Watt)")
plt.legend()
plt.tight_layout()

# === SPEICHERN ===
plt.savefig(OUTPUT_PLOT_PATH)
print(f"[INFO] Plot gespeichert unter: {OUTPUT_PLOT_PATH}")

# === VORHERSAGE AUSGEBEN ===
next_day = forecast.index[-1].strftime("%Y-%m-%d")
predicted_peak = forecast.iloc[-1]
print(f"\n[ERGEBNIS] Prognostizierter Peak am {next_day}: {predicted_peak:.2f} Watt")
