# Mettre à jour les données
update_data:
	python scripts/update_data.py

# Lancer la récupération des échantillons de messages (test/fixtures)
# fetch_samples_data:
# 	python fetch_samples_data.py

# Exécuter la mise à jour complète (update_data et fetch_samples_data)
# full_update: update_data fetch_samples_data

# Lancer les tests
test_fetchers: update_data
	pytest tests/test_fetchers.py

test_usecases: update_data
	pytest tests/test_usecases.py

test_all: update_data
	pytest tests