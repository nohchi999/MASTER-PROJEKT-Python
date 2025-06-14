# etl/load_transformed_to_db.py

from sqlalchemy import create_engine
import pandas as pd

def load_transformed_data(table_name, db_url):
    """
    Lädt die transformierten CSV-Daten in eine Datenbanktabelle.

    :param table_name: Name der Zieltabelle
    :param db_url: Verbindungs-URL zur PostgreSQL-Datenbank
    """
    try:
        print("[INFO] Lade CSV-Datei...")
        df = pd.read_csv("data/full_data_transformed.csv")

        print(f"[INFO] Verbinde mit Datenbank...")
        engine = create_engine(db_url)

        print(f"[INFO] Lade Daten in Tabelle '{table_name}'...")
        df.to_sql(
            table_name,
            schema="smartmeter_data",
            con=engine,
            if_exists="replace",  # ersetzt ggf. alte Tabelle
            index=False
        )

        print(f"[SUCCESS] Daten wurden erfolgreich in Tabelle '{table_name}' geladen.")
    except Exception as e:
        print(f"[ERROR] Fehler beim Laden der Daten: {e}")

# Beispielaufruf
if __name__ == "__main__":
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    table_name = "full_data_transformed"
    load_transformed_data(table_name, db_url)
