from sqlalchemy import create_engine

def load_aggregated_data_to_db(data, db_url, table_name):
    """
    Lädt die transformierten Daten in die Datenbank.

    :param data: DataFrame mit den transformierten Daten
    :param db_url: URL der Datenbank
    :param table_name: Name der Zieltabelle
    """
    try:
        print(f"Starte das Laden der Daten in die Tabelle '{table_name}'...")
        engine = create_engine(db_url)
        data.to_sql(
            table_name,
            con=engine,
            schema="smartmeter_data",  # Schema für die Tabelle
            if_exists="replace",  # Überschreibt die Tabelle, falls sie existiert
            index=False  # Verzichtet auf den Pandas-Index
        )
        print(f"Daten erfolgreich in die Tabelle '{table_name}' geladen.")
    except Exception as e:
        print(f"Fehler beim Laden der Daten: {e}")
