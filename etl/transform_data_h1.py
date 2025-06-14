import pandas as pd

def clean_data(raw_data):
    """
    Bereinigt die Rohdaten, indem Ausreißer entfernt werden.
    """
    print("Bereinigung der Daten gestartet...")

    # Statistische Methode zur Erkennung von Ausreißen: Werte, die mehr als 3 Standardabweichungen vom Mittelwert entfernt sind
    mean = raw_data["1.7.0"].mean()
    std = raw_data["1.7.0"].std()
    clean_data = raw_data[(raw_data["1.7.0"] >= mean - 3 * std) & (raw_data["1.7.0"] <= mean + 3 * std)]

    print(f"Datensätze vor der Bereinigung: {len(raw_data)}")
    print(f"Datensätze nach der Bereinigung: {len(clean_data)}")

    return clean_data

def transform_hypothesis1(data):
    """
    Transformation zur Unterstützung von Hypothese 1 (Verbrauchsunterschiede zwischen Tageszeiten).

    :param data: DataFrame mit den Rohdaten aus der Datenbank
    :return: DataFrame mit stündlicher Aggregation
    """
    print("Starte Transformation für Hypothese 1...")
    # Konvertiere Zeitstempel in ein datetime-Format
    data["time_value"] = pd.to_datetime(data["time_value"])
    # Extrahiere die Stunde aus dem Zeitstempel
    data["hour"] = data["time_value"].dt.hour

    # Gruppiere die Daten nach Stunden und berechne Durchschnitts- und Spitzenverbrauch
    hourly_data = data.groupby("hour").agg(
        avg_consumption=("1.7.0", "mean"),  # Durchschnittsverbrauch pro Stunde
        peak_consumption=("1.7.0", "max")   # Spitzenverbrauch pro Stunde
    ).reset_index()

    print("Transformation für Hypothese 1 abgeschlossen.")

    
    return hourly_data

# Beispielaufruf
if __name__ == "__main__":
    # Beispiel-Daten für Debugging
    example_data = pd.DataFrame({
        "time_value": ["2023-05-06T11:00:00", "2023-05-06T12:00:00", "2023-05-06T12:30:00"],
        "1.7.0": [150, 200, 250]
    })
    print("Starte Bereinigung...")
    cleaned_data = clean_data(example_data)
    print("Starte Transformation...")
    transformed_data = transform_hypothesis1(cleaned_data)
    print("Stündliche Aggregation:")
    print(transformed_data)
