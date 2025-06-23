import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def evaluate_prophet_with_regressors(train_file, test_file):
    """
    Evaluates the Prophet model with additional regressors for Hypothesis 3.

    :param train_file: Path to the training data CSV file
    :param test_file: Path to the testing data CSV file
    """
    print("Starte Prophet-Modell mit zusätzlichen Regressoren...")

    # Lade die Trainings- und Testdaten
    train_data = pd.read_csv(train_file)
    test_data = pd.read_csv(test_file)

    # Konvertiere die Zeitspalte und entferne die Zeitzoneninformationen
    train_data["ds"] = pd.to_datetime(train_data["time_interval"]).dt.tz_localize(None)
    test_data["ds"] = pd.to_datetime(test_data["time_interval"]).dt.tz_localize(None)

    # Zielwert
    train_data["y"] = train_data["peak_consumption"]
    test_data["y"] = test_data["peak_consumption"]

    # Prophet-Modell mit Regressoren
    model = Prophet()
    model.add_regressor("hour")
    model.add_regressor("minute")
    model.add_regressor("peak_consumption_lag1")
    model.add_regressor("peak_consumption_lag2")

    # Trainiere das Modell
    print("Trainiere Prophet-Modell...")
    model.fit(train_data[["ds", "y", "hour", "minute", "peak_consumption_lag1", "peak_consumption_lag2"]])

    # Vorhersage auf den Testdaten
    print("Treffe Vorhersagen...")
    forecast = model.predict(test_data[["ds", "hour", "minute", "peak_consumption_lag1", "peak_consumption_lag2"]])

    # Berechne Metriken
    y_true = test_data["y"]
    y_pred = forecast["yhat"]
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print(f"Prophet Modell mit Regressoren: R² = {r2:.3f}, RMSE = {rmse:.3f}")

    # Speichere die Vorhersagen und zeige Diagramme
    test_data["yhat"] = y_pred
    model.plot(forecast).savefig("visualize/prophet_forecast_with_regressors2.png")
    print("Diagramm gespeichert unter: plots/prophet_forecast_with_regressors2.png")

# Beispielaufruf
if __name__ == "__main__":
    train_file_h3 = "data/10min_data_train.csv"
    test_file_h3 = "data/10min_data_test.csv"
    evaluate_prophet_with_regressors(train_file_h3, test_file_h3)
