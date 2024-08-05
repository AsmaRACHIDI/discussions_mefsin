import json
import os
import logging
import requests
from infrastructure.services.api_fetcher_manager import APIFetcherManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logging.info(f"Data saved successfully to : {filename}")

def fetch_and_save_samples():
    # Répertoires de fixtures
    fixtures_dir = 'tests/fixtures'
    if not os.path.exists(fixtures_dir):
        os.makedirs(fixtures_dir)
    logging.info(f"Fixtures directory : {fixtures_dir} created successfully !")

    try:
        # Fetch DataGouv samples
        data_gouv_fetcher = APIFetcherManager.get_client("data_gouv")
        logging.info("Fetching discussions from DataGouv...")
        data_gouv_discussions = data_gouv_fetcher.fetch_discussions()
        if data_gouv_discussions:
            sample_data_gouv_discussions = data_gouv_discussions[:2]  # Récupérer les deux premiers échantillons
            logging.info(f"Fetched {len(sample_data_gouv_discussions)} discussions from DataGouv !")
            save_json(sample_data_gouv_discussions, os.path.join(fixtures_dir, 'sample_data_gouv_discussions.json'))
        else:
            logging.warning("No discussions fetched from DataGouv")

        logging.info("Fetching datasets from DataGouv...")
        data_gouv_datasets = data_gouv_fetcher.fetch_datasets()
        if data_gouv_datasets:
            sample_data_gouv_datasets = data_gouv_datasets[:2]  # Récupérer les deux premiers échantillons
            logging.info(f"Fetched {len(sample_data_gouv_datasets)} datasets from DataGouv !")
            save_json(sample_data_gouv_datasets, os.path.join(fixtures_dir, 'sample_data_gouv_datasets.json'))
        else:
            logging.warning("No datasets fetched from DataGouv")

        # Fetch DataEco samples
        data_eco_fetcher = APIFetcherManager.get_client("data_eco")
        logging.info("Fetching discussions from DataEco...")
        data_eco_discussions = data_eco_fetcher.fetch_discussions()
        if data_eco_discussions:
            sample_data_eco_discussions = data_eco_discussions[:2]  # Récupérer les deux premiers échantillons
            logging.info(f"Fetched {len(sample_data_eco_discussions)} discussions from DataEco !")
            save_json(sample_data_eco_discussions, os.path.join(fixtures_dir, 'sample_data_eco_discussions.json'))
        else:
            logging.warning("No discussions fetched from DataEco")

        logging.info("Fetching datasets from DataEco...")
        data_eco_datasets = data_eco_fetcher.fetch_datasets()
        if data_eco_datasets:
            sample_data_eco_datasets = data_eco_datasets[:2]  # Récupérer les deux premiers échantillons
            logging.info(f"Fetched {len(sample_data_eco_datasets)} datasets from DataEco !")
            save_json(sample_data_eco_datasets, os.path.join(fixtures_dir, 'sample_data_eco_datasets.json'))
        else:
            logging.warning("No datasets fetched from DataEco")

    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    fetch_and_save_samples()
