import pandas as pd
from sqlalchemy import create_engine

def extract_data(db_url, table_name):
    """
    Extrahiert Daten aus der Datenbanktabelle für Feature-Engineering.

    :param db_url: URL der Datenbank
    :param table_name: Name der Tabelle
    :return: DataFrame mit den Daten
    """
    try:
        print("Verbinde mit der Datenbank...")
        engine = create_engine(db_url)
        query = f"SELECT * FROM {table_name};"
        print(f"Führe Abfrage aus: {query}")
        data = pd.read_sql(query, engine)
        print(f"Erfolgreich {len(data)} Datensätze aus '{table_name}' extrahiert.")
        return data
    except Exception as e:
        print(f"Fehler bei der Datenextraktion: {e}")
        return pd.DataFrame()

def feature_engineering(data):
    """
    Führt Feature-Engineering für Hypothese 1 durch.

    :param data: DataFrame mit den extrahierten Daten
    :return: DataFrame mit neuen Features
    """
    try:
        print("Generiere Features...")

        # Beispiel-Feature: Normierung des Verbrauchs
        data["normalized_avg_consumption"] = data["avg_consumption"] / data["avg_consumption"].max()

        # Beispiel-Feature: Verhältnis zwischen Durchschnitt und Spitze
        data["consumption_ratio"] = data["avg_consumption"] / data["peak_consumption"]

        # Speichern der Ergebnisse als CSV
        data.to_csv("features_hypothesis1.csv", index=False)
        print("Die Features wurden erfolgreich in 'features_hypothesis1.csv' gespeichert.")


        print("Feature-Engineering abgeschlossen.")
        return data
    except Exception as e:
        print(f"Fehler bei der Feature-Generierung: {e}")
        return pd.DataFrame()

# Beispielausführung
if __name__ == "__main__":
    DB_URL = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    TABLE_NAME = "hourly_smartmeter_data"

    # Daten extrahieren
    raw_data = extract_data(DB_URL, TABLE_NAME)

    # Features generieren
    if not raw_data.empty:
        engineered_data = feature_engineering(raw_data)
        print(engineered_data.head())
