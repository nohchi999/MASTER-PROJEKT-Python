import pandas as pd

def transform_hypothesis3(data):
    """
    Transformation zur Unterstützung der Hypothese 3 (Spitzenverbrauchsprognose).
    
    :param data: DataFrame mit den Rohdaten
    :return: DataFrame mit aggregierten Spitzenverbrauchswerten
    """
    print("Starte Transformation für Hypothese 3...")
    
    # Konvertiere Zeitspalte und sortiere nach Zeit
    data["time_value"] = pd.to_datetime(data["time_value"])
    data = data.sort_values("time_value").reset_index(drop=True)

    # Extrahiere Datum (für Aggregation) und Stunde
    data["date"] = data["time_value"].dt.date
    data["hour"] = data["time_value"].dt.hour

    # Aggregiere Daten: Maximalverbrauch pro Tag und Stunde
    peak_data = data.groupby(["date", "hour"], as_index=False).agg(
        peak_consumption=("1.7.0", "max")
    )

    print("Transformation für Hypothese 3 abgeschlossen.")
    return peak_data

# Beispielaufruf
if __name__ == "__main__":
    # Beispiel-Daten
    example_data = pd.DataFrame({
        "time_value": ["2023-05-06T11:00:00", "2023-05-06T12:00:00", "2023-05-06T12:30:00"],
        "1.7.0": [150, 300, 250]
    })
    transformed_data = transform_hypothesis3(example_data)
    print(transformed_data)
