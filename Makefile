# Makefile pour automatiser les tâches de mise à jour et de conversion

# Mettre à jour les données
update_data:
    python scripts/update_data.py

# Convertir les fichiers JSON en CSV
convert_json_to_csv:
    python scripts/json_to_csv.py

# Exécuter la mise à jour complète (update_data suivi de convert_json_to_csv)
full_update: update_data convert_json_to_csv
