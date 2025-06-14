from sqlalchemy import create_engine

def load_data_to_hypothesis1_table(data, table_name, db_url):
    """
    Lädt transformierte Daten in die Datenbank.

    :param data: DataFrame mit den transformierten Daten
    :param table_name: Name der Zieltabelle
    :param db_url: URL der Datenbank
    """
    try:
        print(f"Starte das Laden der Daten in die Tabelle '{table_name}'...")
        engine = create_engine(db_url)
        print("Verbindung zur Datenbank erfolgreich hergestellt.")
        data.to_sql(
            table_name,
            schema="smartmeter_data", # Schema für die Tabelle
            con=engine,
            if_exists="replace",  # Überschreibt bestehende Tabelle
            index=False  # Verzichtet auf den Pandas-Index
        )
        print(f"Transformierte Daten erfolgreich in die Tabelle '{table_name}' geladen.")
    except Exception as e:
        print(f"Fehler beim Laden der Daten in die Tabelle '{table_name}': {e}")

# Beispielaufruf
if __name__ == "__main__":
    import pandas as pd

    # Beispiel-Daten
    example_data = pd.DataFrame({
        "hour": [11, 12, 13],
        "avg_consumption": [150.0, 200.0, 180.0],
        "peak_consumption": [160.0, 220.0, 190.0]
    })

    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    print("Beginne mit dem Laden der Beispiel-Daten...")
    load_data_to_hypothesis1_table(example_data, "hourly_smartmeter_data", db_url)
    print("Laden der Beispiel-Daten abgeschlossen.")
