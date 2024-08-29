# Makefile pour automatiser les tâches de mise à jour et de conversion

# Mettre à jour les données
update_data:
	python scripts/update_data.py

# Lancer la récupération des échantillons de messages (test/fixtures)
fetch_samples_data:
	python fetch_samples_data.py

# Exécuter la mise à jour complète (update_data et fetch_samples_data)
full_update: update_data fetch_samples_data
