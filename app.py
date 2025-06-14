import json
from sqlalchemy import create_engine, text

# Verbindung zur PostgreSQL-Datenbank herstellen
engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data")

# JSON-Daten laden
with open("mqtt_messages_2.json", "r") as file:
    data = json.load(file)  # Lädt alle Einträge aus der JSON-Datei

# Daten in die Datenbank einfügen
for record in data:
    try:
        # Relevante Daten aus dem JSON extrahieren
        row = {
            "1_7_0": float(record["message"].get("1.7.0", 0)),
            "1_8_0": float(record["message"].get("1.8.0", 0)),
            "2_7_0": float(record["message"].get("2.7.0", 0)),
            "2_8_0": float(record["message"].get("2.8.0", 0)),
            "3_8_0": float(record["message"].get("3.8.0", 0)),
            "4_8_0": float(record["message"].get("4.8.0", 0)),
            "16_7_0": float(record["message"].get("16.7.0", 0)),
            "31_7_0": float(record["message"].get("31.7.0", 0)),
            "32_7_0": float(record["message"].get("32.7.0", 0)),
            "51_7_0": float(record["message"].get("51.7.0", 0)),
            "52_7_0": float(record["message"].get("52.7.0", 0)),
            "71_7_0": float(record["message"].get("71.7.0", 0)),
            "72_7_0": float(record["message"].get("72.7.0", 0)),
            "up_time": record["message"].get("uptime", None),
            "time_stamp": record["message"].get("timestamp")
        }

        # SQL-Befehl für das Einfügen
        sql = text("""
            INSERT INTO raw_smartmeter_data (
                time_value, "1.7.0", "1.8.0", "2.7.0", "2.8.0",
                "3.8.0", "4.8.0", "16.7.0",
                "31.7.0", "32.7.0", "51.7.0", "52.7.0", "71.7.0", "72.7.0", uptime
            ) VALUES (
                :time_stamp, :1_7_0, :1_8_0, :2_7_0, :2_8_0,
                :3_8_0, :4_8_0, :16_7_0,
                :31_7_0, :32_7_0, :51_7_0, :52_7_0, :71_7_0, :72_7_0, :up_time
            )
        """)

        # Daten einfügen
        with engine.connect() as conn:
            trans = conn.begin()  # Transaktion starten
            conn.execute(sql, row)
            trans.commit()  # Änderungen speichern

        # Debugging: Erfolgreich eingefügte Daten anzeigen
        print(f"Erfolgreich eingefügt: {row}")

    except Exception as e:
        # Fehlerdetails anzeigen
        print(f"Fehler beim Einfügen des Datensatzes: {record}")
        print(f"Fehlerdetails: {e}")
