import pandas as pd

def transform_to_ten_minute_intervals(data):
    """
    Transformation der Rohdaten in 10-Minuten-Intervalle zur Unterstützung der Hypothese 3.
    
    :param data: DataFrame mit den Rohdaten
    :return: DataFrame mit aggregierten Spitzenverbrauchswerten für 10-Minuten-Intervalle
    """
    print("Starte Transformation in 10-Minuten-Intervalle...")
    
    # Konvertiere Zeitspalte und sortiere nach Zeit
    data["time_value"] = pd.to_datetime(data["time_value"])
    data = data.sort_values("time_value").reset_index(drop=True)

    # Setze den Zeitstempel auf den Start des jeweiligen 10-Minuten-Intervalls
    data["time_interval"] = data["time_value"].dt.floor("10T")

    # Aggregiere Daten: Maximalverbrauch pro 10-Minuten-Intervall
    ten_minute_data = data.groupby("time_interval", as_index=False).agg(
        peak_consumption=("1.7.0", "max"),
        avg_consumption=("1.7.0", "mean"),  # Optional: Durchschnitt pro Intervall
        total_consumption=("1.7.0", "sum")  # Optional: Gesamtverbrauch pro Intervall
    )

    print("Transformation in 10-Minuten-Intervalle abgeschlossen.")
    return ten_minute_data

# Beispielaufruf
if __name__ == "__main__":
    # Beispiel-Daten
    example_data = pd.DataFrame({
        "time_value": ["2023-05-06T11:00:00", "2023-05-06T11:05:00", "2023-05-06T11:15:00", 
                       "2023-05-06T11:25:00", "2023-05-06T11:30:00"],
        "1.7.0": [150, 200, 250, 300, 350]
    })

    transformed_data = transform_to_ten_minute_intervals(example_data)
    print(transformed_data)
