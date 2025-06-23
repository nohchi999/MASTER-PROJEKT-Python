import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import joblib

def feature_importance():
    """
    Führt eine Analyse der Feature Importance durch, basierend auf dem gespeicherten Random Forest Modell.
    """
    # Lade die Trainingsdaten
    train_data = pd.read_csv("data/h3_train.csv")

    # Lade das Modell
    model = joblib.load("models/random_forest_h3.pkl")

    # Features und Zielvariable
    features = train_data.drop(columns=["peak_consumption"])
    target = train_data["peak_consumption"]

    # Prüfe, ob die Dimensionen passen
    print(f"Trainingsdaten: {features.shape}")
    print(f"Zielvariable: {target.shape}")

    # Feature Importance abrufen
    importances = model.feature_importances_
    feature_names = features.columns
    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    print("Feature Importance:")
    print(importance_df)

    # Visualisierung der Feature Importance
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df["Feature"], importance_df["Importance"], color="blue")
    plt.xlabel("Wichtigkeit")
    plt.ylabel("Feature")
    plt.title("Feature Importance für Hypothese 3")
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == "__main__":
    feature_importance()
