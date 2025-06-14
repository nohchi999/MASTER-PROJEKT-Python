from extract_data_h3 import extract_data_h3
from transform_data_h3 import transform_hypothesis3
from load_data_h3 import load_data_to_h3_table

def main_etl_process_h3():
    """
    Hauptprozess für die Durchführung von ETL für Hypothese 3.
    """
    print("Starte ETL-Prozess für Hypothese 3...")

    # Datenbankverbindung
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    source_table = "raw_smartmeter_data"
    target_table = "peak_consumption_data"

    # Extract
    raw_data = extract_data_h3(db_url, source_table)

    # Transform
    transformed_data = transform_hypothesis3(raw_data)

    # Load
    load_data_to_h3_table(transformed_data, target_table, db_url)

    print("ETL-Prozess für Hypothese 3 abgeschlossen.")

if __name__ == "__main__":
    main_etl_process_h3()
