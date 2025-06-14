# Hauptskript: ETL-Prozess für Smartmeter-Daten

from etl.extract_data_h1 import extract_data_for_hypothesis1
from etl.transform_data_h1 import clean_data, transform_hypothesis1
from etl.load_data_h1 import load_data_to_hypothesis1_table

if __name__ == "__main__":
    # Datenbank-Verbindungsdetails
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"

    # 1. Daten extrahieren
    print("Starte die Extraktion der Rohdaten...")
    raw_data = extract_data_for_hypothesis1(db_url, "raw_smartmeter_data")

    # 2. Daten bereinigen
    print("Starte die Bereinigung der Daten...")
    cleaned_data = clean_data(raw_data)

    # 3. Transformation für Hypothese 1
    print("Starte die Transformation für Hypothese 1...")
    transformed_data_h1 = transform_hypothesis1(cleaned_data)


    # 4. Transformierte Daten speichern
    print("Speichere die transformierten Daten...")
    load_data_to_hypothesis1_table(transformed_data_h1, "hourly_smartmeter_data", db_url)

    print("ETL-Prozess für Hypothese 1 abgeschlossen.")
