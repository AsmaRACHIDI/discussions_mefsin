import os
import logging
from infrastructure.services.api_fetcher_manager import APIFetcherManager
from core.config import Config

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Création des répertoires pour les échantillons de données s'il n'existe pas
SAMPLES_DATA_DIR = 'tests/fixtures/samples_data'
os.makedirs(SAMPLES_DATA_DIR, exist_ok=True)

def fetch_and_save_samples():
    try:
        # Initialisation des fetchers via APIFetcherManager
        data_gouv_fetcher = APIFetcherManager.get_client("data_gouv")
        data_eco_fetcher = APIFetcherManager.get_client("data_eco")

        # Fetch DataGouv samples
        data_gouv_discussions = data_gouv_fetcher.fetch_discussions()
        if data_gouv_discussions:
            sample_data_gouv_discussions = data_gouv_discussions[:2]  # Récupérer les deux premiers échantillons
            logging.info(f"Fetched {len(sample_data_gouv_discussions)} discussions from DataGouv")
            data_gouv_fetcher.save_json(sample_data_gouv_discussions, os.path.join(SAMPLES_DATA_DIR, 'sample_data_gouv_discussions.json'))
        else:
            logging.warning("No discussions fetched from DataGouv")

        data_gouv_datasets = data_gouv_fetcher.fetch_datasets()
        if data_gouv_datasets:
            sample_data_gouv_datasets = data_gouv_datasets[:2]  # Récupérer les deux premiers échantillons
            logging.info(f"Fetched {len(sample_data_gouv_datasets)} datasets from DataGouv")
            data_gouv_fetcher.save_json(sample_data_gouv_datasets, os.path.join(SAMPLES_DATA_DIR, 'sample_data_gouv_datasets.json'))
        else:
            logging.warning("No datasets fetched from DataGouv")

        # Fetch DataEco samples
        data_eco_discussions = data_eco_fetcher.fetch_discussions()
        if data_eco_discussions:
            sample_data_eco_discussions = data_eco_discussions[:2]  # Récupérer les deux premiers échantillons
            logging.info(f"Fetched {len(sample_data_eco_discussions)} discussions from DataEco")
            data_eco_fetcher.save_json(sample_data_eco_discussions, os.path.join(SAMPLES_DATA_DIR, 'sample_data_eco_discussions.json'))
        else:
            logging.warning("No discussions fetched from DataEco")

        data_eco_datasets = data_eco_fetcher.fetch_datasets()
        if data_eco_datasets:
            sample_data_eco_datasets = data_eco_datasets[:2]  # Récupérer les deux premiers échantillons
            logging.info(f"Fetched {len(sample_data_eco_datasets)} datasets from DataEco")
            data_eco_fetcher.save_json(sample_data_eco_datasets, os.path.join(SAMPLES_DATA_DIR, 'sample_data_eco_datasets.json'))
        else:
            logging.warning("No datasets fetched from DataEco")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    fetch_and_save_samples()
