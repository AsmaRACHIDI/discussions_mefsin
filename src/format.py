import csv
import json
import os.path

# Fonction pour ouvrir un fichier JSON et charger ses données
def open_json(filename):
    with open(filename, "r", encoding='utf-8') as file:
        data = json.load(file)
        return data

# Fonction pour sauvegarder des données dans un fichier JSON
def dump_json(filename, data):
    with open(filename, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# Fonction pour aplatir un dictionnaire imbriqué
def flatten(dictionary, parent_key='', sep='_'):
    items = []
    for k, v in dictionary.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten(item, f'{new_key}{sep}{i}', sep=sep).items())
                else:
                    items.append((f'{new_key}{sep}{i}', item))
        else:
            items.append((new_key, v))
    return dict(items)

# Fonction pour ajouter des données à un fichier CSV
def append_to_csv(filename, data):
    if not isinstance(data, list):
        raise ValueError("Les données doivent être une liste.")
    if not all(isinstance(d, dict) for d in data):
        raise ValueError("Tous les éléments de la liste doivent être des dictionnaires.")

    result = [flatten(d) for d in data]
    
    if result:
        fieldnames = result[0].keys()
    else:
        fieldnames = []

    with open(filename, "w", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, delimiter=';', fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(result)

# # Test de la fonction append_to_csv
# def test_append_to_csv():
#     # Exemple de données JSON
#     data = [
#         {
#             "discussion_id": "66acd0e35ec1133ac81392cb",
#             "created": "2024-08-02T12:28:18.648000+00:00",
#             "closed": None,
#             "dataset_id": "662c47ee3d303760163d4fc8",
#             "title": "fichier TOPO de Juillet 2024, commune sans aucune voie",
#             "first_message": "Bonjour,\nen intégrant le fichier topo de juillet 2024 en base...",
#             "url_discussion": "https://www.data.gouv.fr/api/1/discussions/66acd0e35ec1133ac81392cb/",
#             "source": "data_gouv",
#             "dataset_title": "Fichier des entités topographiques (TOPO) DGFiP",
#             "dataset_publisher": "",
#             "dataset_created_at": "2024-07-30T18:11:24.456000+00:00",
#             "dataset_updated_at": "2024-07-30T18:11:24.456000+00:00",
#             "dataset_url": "https://www.data.gouv.fr/fr/datasets/fichier-des-entites-topographiques-topo-dgfip-1/"
#         }
#     ]
    
#     csv_filename = "test_output.csv"

#     # Exécuter la fonction
#     append_to_csv(csv_filename, data)

#     # Lire et vérifier le contenu du fichier CSV généré
#     with open(csv_filename, "r", encoding='utf-8') as file:
#         reader = csv.DictReader(file, delimiter=',')
#         rows = list(reader)

#     # Afficher le contenu pour vérification
#     print("Contenu du fichier CSV généré :")
#     for row in rows:
#         print(row)
    

# # Exécuter le test
# test_append_to_csv()
