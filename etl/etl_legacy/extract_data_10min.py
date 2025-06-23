import pandas as pd
from sqlalchemy import create_engine

def extract_raw_data(db_url, table_name):
    """
    Extrahiert Rohdaten aus der angegebenen Datenbanktabelle.

    :param db_url: URL der Datenbank
    :param table_name: Name der Tabelle, aus der die Daten extrahiert werden
    :return: DataFrame mit den extrahierten Rohdaten
    """
    try:
        print("Verbinde mit der Datenbank...")
        engine = create_engine(db_url)
        query = f"SELECT time_value, \"1.7.0\" FROM {table_name};"
        print(f"Führe Abfrage aus: {query}")
        data = pd.read_sql(query, engine)
        print(f"{len(data)} Datensätze erfolgreich extrahiert.")
        return data
    except Exception as e:
        print(f"Fehler bei der Datenextraktion: {e}")
        return pd.DataFrame()
