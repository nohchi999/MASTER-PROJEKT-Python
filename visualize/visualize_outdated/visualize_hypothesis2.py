import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# 1) Verbindung zur Datenbank
db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
table_name = "supply_vs_consumption_data"
engine = create_engine(db_url)

# 2) Daten aus der Tabelle laden
query = f"""
    SELECT 
        date,
        hour,
        total_consumption,
        total_generation,
        net_generation
    FROM {table_name};
"""
df = pd.read_sql(query, engine)

# 3) Datum+Stunde in eine echte Zeitspalte umwandeln und sortieren
df['datetime'] = pd.to_datetime(df['date']) + pd.to_timedelta(df['hour'], 'h')
df = df.sort_values('datetime').reset_index(drop=True)

# 4) Zwei Plots untereinander: (a) Verbrauch vs. Erzeugung (b) Netto-Einspeisung
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# (a) Verbrauch vs. Erzeugung
ax1.plot(df['datetime'], df['total_consumption'], label='Verbrauch (1.8.0)', color='blue')
ax1.plot(df['datetime'], df['total_generation'], label='Einspeisung (3.8.0)', color='orange')
ax1.set_ylabel('kWh')
ax1.set_title('Verbrauch vs. Erzeugung über die Zeit')
ax1.legend()
ax1.grid(True)

# (b) Netto-Einspeisung
ax2.plot(df['datetime'], df['net_generation'], label='Netto-Einspeisung (3.8.0 - 1.8.0)', color='green')
ax2.axhline(0, color='red', linestyle='--')
ax2.set_xlabel('Datum & Stunde')
ax2.set_ylabel('kWh')
ax2.set_title('Netto-Einspeisung')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
