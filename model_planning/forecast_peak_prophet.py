import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os
import numpy as np

# Lade Daten
df = pd.read_csv("data/full_data_transformed.csv", parse_dates=["timestamp"])

# Tagespeaks berechnen
df["date"] = df["timestamp"].dt.date
daily_peaks = df.groupby("date")["1.7.0"].max().reset_index()
daily_peaks.columns = ["ds", "y"]

# 2. Log-Transformation (aber nur gültige Werte)
# --------------------------------------------
daily_peaks = daily_peaks[daily_peaks["y"] > 0]  # Prophet mag keine 0 oder negativen Werte
daily_peaks["y_log"] = np.log1p(daily_peaks["y"])

# Filtere unrealistische Werte
# daily_peaks = daily_peaks[daily_peaks["y"] >= 2000]
daily_peaks = daily_peaks[(daily_peaks['y'] >= 4000) & (daily_peaks['y'] <= 7000)]


# Prophet-Modell
model = Prophet(seasonality_mode='multiplicative')
model.add_seasonality(name='weekly', period=7, fourier_order=3)
model.fit(daily_peaks)

# Zukunft prognostizieren (7 Tage)
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)

# Visualisierung
fig = model.plot(forecast)
plt.title("Prognose der täglichen Spitzenlast (1.7.0) in Watt")
plt.xlabel("Datum")
plt.ylabel("Täglicher Peak (Watt)")
plt.tight_layout()
# plt.savefig("visualize/prophet_forecast_peak_log.png")
plt.savefig("visualize/prophet_forecast_peak_ignore_extrema_log.png")

# Ergebnis
print(f"Prognostizierter Peak am {forecast['ds'].iloc[-1]}: {forecast['yhat'].iloc[-1]:.2f} Watt")
