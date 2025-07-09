import pandas as pd
from sklearn.model_selection import train_test_split

def split_train_test(input_file, output_train_file, output_test_file, test_size=0.2, random_state=42):
    """
    Teilt die Daten in Trainings- und Testdatensätze auf und speichert sie als CSV-Dateien.

    :param input_file: Pfad zur Eingabedatei (CSV)
    :param output_train_file: Pfad zur Ausgabedatei für Trainingsdaten
    :param output_test_file: Pfad zur Ausgabedatei für Testdaten
    :param test_size: Anteil der Testdaten (Standard: 20%)
    :param random_state: Seed für die Zufallsauswahl (Standard: 42)
    """
    try:
        print(f"Lade Daten aus: {input_file}")
        data = pd.read_csv(input_file)
        
        print("Teile die Daten in Trainings- und Testdatensätze auf...")
        train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)

        print(f"Speichere Trainingsdaten in: {output_train_file}")
        train_data.to_csv(output_train_file, index=False)

        print(f"Speichere Testdaten in: {output_test_file}")
        test_data.to_csv(output_test_file, index=False)

        print("Train-Test-Splitting abgeschlossen.")
    except Exception as e:
        print(f"Fehler beim Train-Test-Splitting: {e}")

# Beispielaufruf
if __name__ == "__main__":

    # H3-Daten
    input_file_h3 = "data/10min_data_features.csv"
    train_file_h3 = "data/10min_data_train.csv"
    test_file_h3 = "data/10min_data_test.csv"
    split_train_test(input_file_h3, train_file_h3, test_file_h3)
