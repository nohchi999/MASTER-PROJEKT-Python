from extract_data_10min import extract_raw_data
from transform_data_10min import transform_to_ten_minute_intervals
from load_data_10min import load_aggregated_data_to_db

def main_etl_h3():
    """
    Führt den ETL-Prozess für Hypothese 3 (10-Minuten-Intervalle) durch.
    """
    # Datenbankverbindungsdetails
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    raw_table_name = "raw_smartmeter_data"
    aggregated_table_name = "ten_minute_smartmeter_data"

    # ETL-Prozess
    print("Starte ETL-Prozess für Hypothese 3...")
    raw_data = extract_raw_data(db_url, raw_table_name)
    if raw_data.empty:
        print("Keine Rohdaten gefunden. ETL-Prozess abgebrochen.")
        return

    transformed_data = transform_to_ten_minute_intervals(raw_data)
    load_aggregated_data_to_db(transformed_data, db_url, aggregated_table_name)
    print("ETL-Prozess für 10min-Interval abgeschlossen.")

if __name__ == "__main__":
    main_etl_h3()
