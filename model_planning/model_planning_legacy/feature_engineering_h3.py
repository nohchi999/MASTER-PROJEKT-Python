import pandas as pd
from sqlalchemy import create_engine

def generate_features_h3(db_url, table_name, output_file):
    """
    Generiert Features für Hypothese 3 (Spitzenverbrauchsprognose) und speichert sie in einer CSV-Datei.

    :param db_url: URL der Datenbank
    :param table_name: Name der Tabelle mit aggregierten Daten
    :param output_file: Pfad zur Ausgabedatei (CSV)
    """
    try:
        print("Verbinde mit der Datenbank...")
        engine = create_engine(db_url)

        # Daten aus der Tabelle laden
        query = f"SELECT * FROM {table_name};"
        print(f"Führe Abfrage aus: {query}")
        data = pd.read_sql(query, engine)

        print("Generiere Features...")
        # Konvertiere Zeitstempel
        data["hour"] = data["hour"].astype(int)  # Stunde bleibt als numerische Spalte
        data["date"] = pd.to_datetime(data["date"])
        data["weekday"] = data["date"].dt.weekday
        data["is_weekend"] = data["weekday"].apply(lambda x: 1 if x >= 5 else 0)

        # Lag-Features erstellen
        data["peak_consumption_lag1"] = data["peak_consumption"].shift(1)
        data["peak_consumption_lag2"] = data["peak_consumption"].shift(2)

        # NaN-Werte entfernen, die durch Lag-Features entstehen
        data = data.dropna().reset_index(drop=True)

        # Wichtige Spalten auswählen
        features = data[["hour", "weekday", "is_weekend", "peak_consumption", 
                         "peak_consumption_lag1", "peak_consumption_lag2"]]

        print(f"Speichere Features in: {output_file}")
        features.to_csv(output_file, index=False)
        print("Feature-Generierung für Hypothese 3 abgeschlossen.")
    except Exception as e:
        print(f"Fehler bei der Feature-Generierung: {e}")

# Beispielaufruf
if __name__ == "__main__":
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    table_name = "peak_consumption_data"
    output_file = "data/h3_features.csv"

    generate_features_h3(db_url, table_name, output_file)
