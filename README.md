# Smart-Meter Master-Projekt

Dieses Repository sammelt alle Skripte rund um ein Smart-Meter-Projekt. Ziel ist es, Rohdaten aus einer MQTT-Quelle zu verarbeiten, in eine PostgreSQL-Datenbank zu laden und anschließend verschiedene Analysen sowie Prognosen durchzuführen. Das Projekt entstand im Rahmen eines Master-Projekts und enthält neben aktuellen Skripten auch ältere, als „legacy“ gekennzeichnete Varianten.

---

## Inhaltsverzeichnis

1. [Verzeichnisstruktur](#verzeichnisstruktur)  
2. [Voraussetzungen](#voraussetzungen)  
3. [Schnellstart](#schnellstart)  
4. [ETL-Pipeline](#etl-pipeline)  
5. [Analysen & Modellierung](#analysen--modellierung)  
6. [Visualisierung](#visualisierung)  
7. [Legacy-Skripte](#legacy-skripte)  
8. [Ausblick](#ausblick)  

---

## Verzeichnisstruktur

```
.
├── app.py                    # Beispielskript zum Import einer JSON-Datei in die DB
├── etl/                      # Hauptordner für ETL-Skripte
│   ├── extract_data_full.py
│   ├── transform_data_full.py
│   ├── load_data_full.py
│   └── etl_legacy/           # Ältere oder experimentelle ETL-Varianten
├── model_planning/           # Statistische Analysen und Prognosen
│   ├── descriptive_statistics_full.py
│   ├── hypothesis_test_full.py
│   ├── forecast_peak_prophet.py
│   ├── forecast_peak_holtwinters.py
│   └── ...
├── visualize/                # Ergebnisgrafiken (PNG-Dateien)
│   └── visualize_outdated/   # Ältere Visualisierungen
└── README.md                 # Diese Datei
```

> Während der Verarbeitung werden weitere Dateien (z. B. im Ordner `data/`) erzeugt, die jedoch nicht Teil des Repositories sind.

---

## Voraussetzungen

- **Python**: Version 3.x (empfohlen ≥ 3.9)  
- **Python-Pakete** (Auszug):
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `sqlalchemy`
  - `statsmodels`
  - `prophet`
  - `scikit-learn`
  - `psycopg2-binary`  
  _(je nach Skript können weitere Pakete erforderlich sein)_
- **PostgreSQL-Datenbank**:
  - Lokale Instanz  
  - Datenbank: `smartmeter_data`  
  - Benutzer: `postgres`  
  - Passwort: `password`  
  (Anpassbar in den Skripten)
- **JSON-Rohdaten**:
  - `mqtt_messages_2.json` muss im Hauptverzeichnis liegen.

---

## Schnellstart

1. **Abhängigkeiten installieren**  
   ```bash
   pip install pandas numpy matplotlib seaborn                sqlalchemy statsmodels prophet                scikit-learn psycopg2-binary
   ```
   *(Alternativ: virtuelles Environment einrichten)*

2. **Datenbank vorbereiten**  
   ```sql
   CREATE DATABASE smartmeter_data;
   ```

3. **ETL-Skripte ausführen**  
   ```bash
   python etl/extract_data_full.py       # JSON → CSV
   python etl/transform_data_full.py     # Bereinigung & Feature-Erzeugung
   python etl/load_data_full.py          # CSV → PostgreSQL
   ```

4. **Analyse oder Modell starten**  
   ```bash
   python model_planning/descriptive_statistics_full.py
   python model_planning/forecast_peak_prophet.py
   ```

5. **Grafiken prüfen**  
   - Ergebnisgrafiken liegen im Ordner `visualize/`.

---

## ETL-Pipeline

1. **Extraktion** (`extract_data_full.py`)  
   - Liest die JSON-Datei ein und schreibt alle Messwerte nach `data/full_data.csv`.  
2. **Transformation** (`transform_data_full.py`)  
   - Zeitstempel → `datetime`  
   - Messspalten → numerische Typen  
   - Entfernt Duplikate & Extremwerte  
   - Tag/Nacht-Kennzeichnung  
   - Ergebnis → `data/full_data_transformed.csv`  
3. **Laden** (`load_data_full.py`)  
   - Überträgt die transformierten Daten in die PostgreSQL-Tabelle `smartmeter_data.full_data_transformed`.  
4. **Alternative** (`app.py`)  
   - Import einer JSON-Datei direkt in die Tabelle `raw_smartmeter_data`.

---

## Analysen & Modellierung

Alle Skripte liegen im Ordner `model_planning/`:

- **Deskriptive Statistik**  
  `descriptive_statistics_full.py` → Histogramme, Boxplots, Verbrauchsstatistiken.  
- **Hypothesentests**  
  - `hypothesis_test_full.py`  
  - `hypothesis_test_greater.py`  
  - `hypothesis_test_two_sided.py`  
  - `hypothesis_test_precise.py`  
  (Mann-Whitney-U-Test: Tag vs. Nacht)  
- **Prognosen**  
  - `forecast_peak_prophet.py`  
  - `forecast_peak_holtwinters.py`  

Ergebnisse → Grafiken im Ordner `visualize/`.

---

## Visualisierung

Im Ordner `visualize/` befinden sich PNG-Dateien wie:

- Histogramme & Boxplots des Verbrauchs  
- Heatmaps nach Stunden & Wochentagen  
- Tägliche Peaks & Prognosekurven  

Ältere Varianten → `visualize/visualize_outdated/`.

---

## Legacy-Skripte

- `etl/etl_legacy/`  
- `model_planning/model_planning_outdated/`  

Enthalten experimentelle Ansätze (10-Minuten-Aggregation, erweitertes Feature-Engineering). Dienen als Referenz, meist nicht mehr erforderlich.

---

## Ausblick

- `requirements.txt` ergänzen  
- Automatisierte Tests integrieren  
- Docker-Setup & CI-Pipeline aufsetzen  
