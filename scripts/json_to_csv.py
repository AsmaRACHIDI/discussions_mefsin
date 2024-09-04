import csv
import os
from infrastructure.repositories.tinydb_comment_repository import TinyDBCommentRepository


def json_to_csv(json_data, csv_file_path):
    # Vérifier si le répertoire de sortie existe, sinon le créer
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    # Extraire les champs pertinents des données JSON
    fields = ["id", "title", "discussion", "prediction_motif", "prediction_sous_motif"]

    with open(csv_file_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for entry in json_data:
            writer.writerow(
                {
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "discussion": entry.get("discussion"),
                    "prediction_motif": entry.get("prediction_motif"),
                    "prediction_sous_motif": entry.get("prediction_sous_motif"),
                }
            )

    print(f"Data has been successfully exported to {csv_file_path}")


if __name__ == "__main__":
    # Charger les données depuis TinyDB
    repository = TinyDBCommentRepository()
    json_data = repository.get_all_comments()

    # Chemin du fichier CSV de sortie
    csv_file_path = os.path.join("app", "static", "data", "asma.csv")

    # Conversion JSON en CSV
    json_to_csv(json_data, csv_file_path)
