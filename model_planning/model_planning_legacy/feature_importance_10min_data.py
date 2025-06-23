import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_feature_importance(model_path, feature_names):
    """
    Analysiert die Feature-Wichtigkeit eines gespeicherten Random Forest Modells.

    :param model_path: Pfad zum gespeicherten Random Forest Modell (joblib-Datei).
    :param feature_names: Liste der Feature-Namen, die im Modell verwendet wurden.
    """
    try:
        print("Lade Modell...")
        model = joblib.load(model_path)
        
        if not hasattr(model, "feature_importances_"):
            raise ValueError("Das geladene Modell unterstützt keine Feature-Wichtigkeit.")

        print("Berechne Feature-Wichtigkeiten...")
        feature_importances = model.feature_importances_

        # Daten in ein DataFrame umwandeln
        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": feature_importances
        }).sort_values(by="Importance", ascending=False)

        print("Feature-Wichtigkeiten:")
        print(importance_df)

        # Visualisierung der Feature-Wichtigkeiten
        plt.figure(figsize=(10, 6))
        sns.barplot(x="Importance", y="Feature", data=importance_df, palette="viridis")
        plt.title("Feature Importance für Hypothese 3")
        plt.xlabel("Wichtigkeit")
        plt.ylabel("Feature")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Fehler bei der Feature-Wichtigkeitsanalyse: {e}")

# Beispielaufruf
if __name__ == "__main__":
    model_path = "models/random_forest_10min_data.pkl"  # Pfad zum gespeicherten Modell
    feature_names = ["hour","minute", "weekday", "is_weekend", "peak_consumption_lag1", "peak_consumption_lag2"]
    analyze_feature_importance(model_path, feature_names)
