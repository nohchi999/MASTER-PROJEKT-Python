import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import joblib

def evaluate_model(model, X_train, X_test, y_train, y_test):
    """
    Trainiert und bewertet ein Modell anhand von Trainings- und Testdaten.

    :param model: Das zu bewertende Modell
    :param X_train: Trainingsfeatures
    :param X_test: Testfeatures
    :param y_train: Trainingszielwerte
    :param y_test: Testzielwerte
    :return: Metriken (R² und RMSE)
    """
    print("Starte Training des Modells...")
    model.fit(X_train, y_train)
    print("Training abgeschlossen.")

    # Vorhersagen treffen
    y_pred = model.predict(X_test)

    # Metriken berechnen
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"Evaluierung abgeschlossen: R² = {r2:.3f}, RMSE = {rmse:.3f}")
    return r2, rmse


def model_selection_h3(train_file, test_file, model_output_path="models/random_forest_10min_data.pkl"):
    """
    Führt die Modellauswahl für Hypothese 3 basierend auf 10-Minuten-Intervall-Daten durch und speichert das beste Modell.

    :param train_file: Pfad zu den Trainingsdaten (CSV)
    :param test_file: Pfad zu den Testdaten (CSV)
    :param model_output_path: Pfad, unter dem das Modell gespeichert wird
    """
    print("Starte Modellauswahl für Hypothese 3 (10-Minuten-Intervalle)...")
    train_data = pd.read_csv(train_file)
    test_data = pd.read_csv(test_file)

    # Prüfen, ob die notwendigen Features vorhanden sind
    required_features = ["hour", "minute", "weekday", "is_weekend", "peak_consumption_lag1", "peak_consumption_lag2"]
    for feature in required_features:
        if feature not in train_data.columns or feature not in test_data.columns:
            raise ValueError(f"Feature '{feature}' fehlt in den Trainings- oder Testdaten.")

    # Features und Zielwert
    X_train = train_data[required_features]
    y_train = train_data["peak_consumption"]
    X_test = test_data[required_features]
    y_test = test_data["peak_consumption"]

    # Random Forest Regressor
    rf_model = RandomForestRegressor(random_state=42, n_estimators=100)
    r2, rmse = evaluate_model(rf_model, X_train, X_test, y_train, y_test)
    print(f"Random Forest Regressor: R² = {r2:.3f}, RMSE = {rmse:.3f}")

    # Speichere das trainierte Modell
    print(f"Speichere das Modell unter: {model_output_path}")
    joblib.dump(rf_model, model_output_path)
    print("Modell erfolgreich gespeichert.")

# Beispielaufruf
if __name__ == "__main__":
    # Hypothese 3
    train_file_h3 = "data/10min_data_train.csv"  # Neue CSV-Datei mit 10-Minuten-Intervall-Trainingsdaten
    test_file_h3 = "data/10min_data_test.csv"    # Neue CSV-Datei mit 10-Minuten-Intervall-Testdaten
    model_selection_h3(train_file_h3, test_file_h3)
