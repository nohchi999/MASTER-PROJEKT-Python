import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Verbindung zur PostgreSQL-Datenbank herstellen
db_url = "postgresql+psycopg2://postgres:password@localhost:5432/smartmeter_data"
engine = create_engine(db_url)

# Daten aus der Tabelle laden
query = "SELECT * FROM hourly_smartmeter_data;"
data = pd.read_sql(query, engine)

# Daten sortieren (sicherstellen, dass die Stunden in der richtigen Reihenfolge sind)
data = data.sort_values(by="hour")

# Visualisierung erstellen
plt.figure(figsize=(12, 6))

# Durchschnittsverbrauch plotten
plt.plot(data["hour"], data["avg_consumption"], label="Durchschnittlicher Verbrauch", marker="o")

# Spitzenverbrauch plotten
plt.plot(data["hour"], data["peak_consumption"], label="Spitzenverbrauch", marker="o")

# Titel und Achsenbeschriftungen hinzufügen
plt.title("Energieverbrauch nach Stunde (Aggregiert)")
plt.xlabel("Stunde des Tages")
plt.ylabel("Verbrauch (Einheiten)")
plt.xticks(range(0, 24))  # Stunden von 0 bis 23
plt.grid(True)
plt.legend()

# Diagramm anzeigen
plt.tight_layout()
plt.show()
