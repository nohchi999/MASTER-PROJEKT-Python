# model_planning/forecast_peak_prophet.py

import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import os

# -------------------------------
# 1. Daten laden
# -------------------------------
print("[INFO] Lade transformierte CSV-Datei...")
df = pd.read_csv("data/full_data_transformed.csv", parse_dates=["timestamp"])

# -------------------------------
# 2. Tages-Peak berechnen (1.7.0)
# -------------------------------
print("[INFO] Berechne Tagesmaxima für 1.7.0...")
df["date"] = df["timestamp"].dt.date
daily_peaks = df.groupby("date")["1.7.0"].max().reset_index()
daily_peaks.columns = ["ds", "y"]

# Optional: Entferne Tage mit unrealistischen Werten (z. B. 0)
daily_peaks = daily_peaks[daily_peaks["y"] > 0]

# -------------------------------
# 3. Prophet-Modell trainieren
# -------------------------------
print("[INFO] Trainiere Prophet-Modell...")
model = Prophet(daily_seasonality=True)
model.fit(daily_peaks)

# -------------------------------
# 4. Prognose generieren
# -------------------------------
future = model.make_future_dataframe(periods=1)
forecast = model.predict(future)

# -------------------------------
# 5. Ergebnis visualisieren
# -------------------------------
print("[INFO] Speichere Forecast-Plot...")
fig = model.plot(forecast)
plt.title("Prognose Tages-Peakverbrauch (1.7.0)")
plt.xlabel("Datum")
plt.ylabel("Peak-Leistung (Watt)")
output_path = os.path.join("visualize", "prophet_forecast_peak.png")
fig.savefig(output_path)

# -------------------------------
# 6. Prognosewert ausgeben
# -------------------------------
predicted_value = forecast.iloc[-1]["yhat"]
predicted_date = forecast.iloc[-1]["ds"].date()

print("\n=== PROPHET PROGNOSE ===")
print(f"Prognostizierter Peak am {predicted_date}: {predicted_value:.2f} Watt")
print(f"[INFO] Plot gespeichert unter: {output_path}")
