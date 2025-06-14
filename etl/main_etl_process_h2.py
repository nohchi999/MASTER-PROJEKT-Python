from extract_data_h2 import extract_data_for_hypothesis2
from transform_data_h2 import clean_data, transform_hypothesis2
from load_data_h2 import load_data_to_hypothesis2_table

def main_etl_hypothesis2():
    """
    Haupt-ETL-Prozess für Hypothese 2: Einspeisung vs. Verbrauch.
    """
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    table_name_raw = "raw_smartmeter_data"
    table_name_transformed = "supply_vs_consumption_data"

    # 1. Daten extrahieren
    print("[1] Extrahiere Daten...")
    raw_data = extract_data_for_hypothesis2(db_url, table_name_raw)

    if raw_data.empty:
        print("Keine Daten gefunden. Prozess wird beendet.")
        return

    # 2. Daten bereinigen
    print("[2] Bereinige Daten...")
    cleaned_data = clean_data(raw_data)

    # 3. Transformation durchführen
    print("[3] Transformiere Daten...")
    transformed_data = transform_hypothesis2(cleaned_data)

    # 4. Transformierte Daten speichern
    print("[4] Speichere transformierte Daten...")
    load_data_to_hypothesis2_table(transformed_data, table_name_transformed, db_url)

    print("ETL-Prozess für Hypothese 2 abgeschlossen.")

if __name__ == "__main__":
    main_etl_hypothesis2()
