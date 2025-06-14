import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def visualize_smoothed_peak_consumption(db_url, table_name):
    """
    Visualisiert die Spitzenverbrauchswerte aus der Datenbank mit einer geglätteten Darstellung.

    :param db_url: URL der Datenbank
    :param table_name: Name der Tabelle mit den Spitzenverbrauchswerten
    """
    try:
        print("Verbinde mit der Datenbank...")
        engine = create_engine(db_url)
        
        # Daten aus der Tabelle laden
        query = f"SELECT * FROM {table_name};"
        print(f"Führe Abfrage aus: {query}")
        data = pd.read_sql(query, engine)
        
        # Konvertiere das Datum in ein datetime-Format
        data["date"] = pd.to_datetime(data["date"])
        data["timestamp"] = data["date"] + pd.to_timedelta(data["hour"], unit="h")

        # Optional: Glättung der Daten (z. B. Moving Average)
        data["smoothed_peak"] = data["peak_consumption"].rolling(window=24, min_periods=1).mean()

        print("Starte die Visualisierung...")
        plt.figure(figsize=(16, 8))

        # Visualisierung der geglätteten Daten
        plt.plot(data["timestamp"], data["smoothed_peak"], label="Geglätteter Spitzenverbrauch (kWh)", color="darkblue", linewidth=2)

        # Verbesserte Achsenbeschriftung
        plt.title("Geglätteter Spitzenverbrauch über die Zeit", fontsize=16)
        plt.xlabel("Zeit (Datum und Stunde)", fontsize=14)
        plt.ylabel("Spitzenverbrauch (kWh)", fontsize=14)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)

        # Stundenachsen-Beschriftungen vereinfachen
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))  # Maximal 15 Ticks
        plt.grid(True, linestyle="--", alpha=0.6)

        # Legende und Layout optimieren
        plt.legend(fontsize=12)
        plt.tight_layout()

        # Visualisierung anzeigen
        plt.show()
        print("Visualisierung abgeschlossen.")

    except Exception as e:
        print(f"Fehler bei der Visualisierung: {e}")

# Beispielaufruf
if __name__ == "__main__":
    db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
    table_name = "peak_consumption_data"
    visualize_smoothed_peak_consumption(db_url, table_name)
