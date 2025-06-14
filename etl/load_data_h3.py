from sqlalchemy import create_engine

def load_data_to_h3_table(data, table_name, db_url):
    """
    Lädt transformierte Daten für Hypothese 3 in die Datenbank.

    :param data: DataFrame mit den transformierten Daten
    :param table_name: Name der Zieltabelle
    :param db_url: URL der Datenbank
    """
    try:
        print(f"Starte das Laden der Daten in die Tabelle '{table_name}'...")
        engine = create_engine(db_url)
        data.to_sql(
            table_name,
            schema="smartmeter_data",  # Schema für die Tabelle
            con=engine,
            if_exists="replace",  # Überschreibt bestehende Tabelle
            index=False  # Verzichtet auf den Pandas-Index
        )
        print(f"Daten erfolgreich in die Tabelle '{table_name}' geladen.")
    except Exception as e:
        print(f"Fehler beim Laden der Daten in die Tabelle '{table_name}': {e}")

# Beispielaufruf
if __name__ == "__main__":
    import pandas as pd

    # Beispiel-Daten
    example_data = pd.DataFrame({
        "date": ["2023-05-06", "2023-05-06"],
        "hour": [11, 12],
        "peak_consumption": [300, 250]
    })

    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    load_data_to_h3_table(example_data, "peak_consumption_data", db_url)
