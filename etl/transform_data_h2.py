import pandas as pd

def clean_data(raw_data):
    """
    Bereinigt die Rohdaten, indem Ausreißer entfernt werden.
    """
    print("Bereinigung der Daten gestartet...")

    # Entfernen von Nullwerten
    clean_data = raw_data.dropna(subset=["1.8.0", "3.8.0"])

    print(f"Datensätze vor der Bereinigung: {len(raw_data)}")
    print(f"Datensätze nach der Bereinigung: {len(clean_data)}")
    return clean_data

def transform_hypothesis2(data):
    """
    Transformation zur Unterstützung der Hypothese 
    "Einspeisung (3.8.0) könnte zu bestimmten Zeiten 
    höher sein als Verbrauch (1.8.0)".
    """
    # 1) Zeitspalte konvertieren und Daten sortieren
    data["time_value"] = pd.to_datetime(data["time_value"])
    data = data.sort_values("time_value").reset_index(drop=True)

    # 2) Differenzen berechnen (Zählerstände -> Verbrauch/Einspeisung pro Messintervall)
    data["delta_consumption"] = data["1.8.0"].diff()
    data["delta_generation"] = data["3.8.0"].diff()

    # 3) Negative Differenzen ggf. als Ausreißer/Rollover behandeln und auf 0/Nan setzen
    data.loc[data["delta_consumption"] < 0, "delta_consumption"] = None
    data.loc[data["delta_generation"] < 0, "delta_generation"] = None

    # 4) NaN durch 0 ersetzen
    data["delta_consumption"] = data["delta_consumption"].fillna(0)
    data["delta_generation"] = data["delta_generation"].fillna(0)

    # 5) Netto-Einspeisung: Erzeugung - Verbrauch
    data["net_generation"] = data["delta_generation"] - data["delta_consumption"]

    # 6) Gruppieren nach Tag + Stunde (so vermischst du nicht unterschiedliche Tage)
    data["date"] = data["time_value"].dt.date
    data["hour"] = data["time_value"].dt.hour
    grouped_data = data.groupby(["date", "hour"], as_index=False).agg(
        total_consumption=("delta_consumption", "sum"),
        total_generation=("delta_generation", "sum"),
        net_generation=("net_generation", "sum")
    )

    return grouped_data
