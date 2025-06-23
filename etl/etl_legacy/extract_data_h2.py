import pandas as pd
from sqlalchemy import create_engine

def extract_data_for_hypothesis2(db_url, table_name):
    """
    Extrahiert Rohdaten aus der angegebenen Datenbanktabelle für die Hypothese 2.

    :param db_url: URL der Datenbank
    :param table_name: Name der Tabelle, aus der Daten extrahiert werden
    :return: DataFrame mit den extrahierten Rohdaten
    """
    try:
        print(f"Verbinde mit der Datenbank: {db_url}")
        engine = create_engine(db_url)
        query = f"SELECT time_value, \"1.8.0\", \"3.8.0\" FROM {table_name};"
        print(f"Führe Abfrage aus: {query}")
        data = pd.read_sql(query, engine)
        print(f"{len(data)} Datensätze erfolgreich aus der Tabelle '{table_name}' extrahiert.")
        return data
    except Exception as e:
        print(f"Fehler bei der Extraktion aus der Datenbank: {e}")
        return pd.DataFrame()

# Beispielaufruf (falls benötigt)
if __name__ == "__main__":
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    table_name = "raw_smartmeter_data"
    data = extract_data_for_hypothesis2(db_url, table_name)
    print(data.head())
