import csv
import json
import os.path


# Fonction pour ouvrir un fichier JSON et charger ses données
def open_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        return data


# Fonction pour sauvegarder des données dans un fichier JSON
def dump_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


# Fonction pour aplatir un dictionnaire imbriqué
def flatten(dictionary, parent_key="", sep="_"):
    flattened_data = {}
    for k, v in dictionary.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            flattened_data.update(flatten(v, new_key, sep=sep))
        else:
            flattened_data[new_key] = v
    return flattened_data


# Fonction pour ajouter des données à un fichier CSV
def append_to_csv(filename, data):
    # Aplatis les données pour les rendre compatibles avec l'écriture CSV
    result = [flatten(d) for d in data]
    # Ouvre le fichier CSV en mode écriture
    with open(filename, "w", newline="") as file:
        # Crée un objet writer pour écrire dans le fichier CSV avec le délimiteur ';' et les en-têtes basées sur les clés des données
        writer = csv.DictWriter(file, delimiter=';', fieldnames=result[0].keys())
        # Écrit les en-têtes dans le fichier CSV
        writer.writeheader()
        # Écrit les données dans le fichier CSV
        writer.writerows(result)
