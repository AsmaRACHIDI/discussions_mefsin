import requests
import logging
import os
from domain.gateways import BaseFetcher
from typing import List, Dict, Optional
from core.config import Config
import json

HEADERS = {"Authorization": f"Apikey {Config.API_KEY}"}

UNFORMATTED_DATA_DIR = 'tests/fixtures/unformatted_data'
FORMATTED_DATA_DIR = 'tests/fixtures/formatted_data'

# Création des répertoires s'ils n'existent pas
os.makedirs(UNFORMATTED_DATA_DIR, exist_ok=True)
os.makedirs(FORMATTED_DATA_DIR, exist_ok=True)

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataGouvFetcher(BaseFetcher):
    def fetch_discussions(self) -> Optional[List[Dict]]:
        logging.info("Fetching discussions from data.gouv.fr API :")
        try:
            response = requests.get(self.discussions_url)
            response.raise_for_status()
            data_json = response.json()
            logging.info(f"Fetched {len(data_json)} discussions from data.gouv.fr")

            # Enregistrement des données non formatées
            self.save_json(data_json, f'{UNFORMATTED_DATA_DIR}/unformatted_data_gouv_discussions.json')

            formatted_discussions = self.format_discussions(data_json)

            # Enregistrement des données formatées
            self.save_json(formatted_discussions, f'{FORMATTED_DATA_DIR}/formatted_data_gouv_discussions.json')
            
            return formatted_discussions
        except requests.RequestException as e:
            logging.error(f"Request error: {e}")
            return None

    def format_discussions(self, discussions: List[Dict]) -> List[Dict]:
        formatted_discussions = []
        for discussion in discussions:
            formatted_discussion = {
                "discussion_id": discussion["id"],
                "created": discussion["created"],
                "closed": discussion["closed"],
                "dataset_id": discussion["subject"]["id"],
                "title": discussion["title"],
                "first_message": discussion["discussion"][0]["content"],
                "url_discussion": discussion["url"],
                "source": "data_gouv"
            }
            formatted_discussions.append(formatted_discussion)
        return formatted_discussions

    def fetch_datasets(self) -> Optional[List[Dict]]:
        logging.info("Fetching datasets from data.gouv.fr API :")
        datasets = []
        page = 1
        try:
            while True:
                url = f"{self.datasets_url}?page={page}"
                response = requests.get(url)
                # On vérifie d'abord l'existence de la page ou la présence de données dans la page avant de lancer la récupération
                if response.status_code == 404 or not response.json().get("data"):
                    break
                response.raise_for_status()
                data = response.json()
                datasets.extend(data["data"])
                page += 1
            logging.info(f"Fetched {len(datasets)} datasets from data.gouv.fr")

            # Enregistrement des données non formatées
            self.save_json(datasets, f'{UNFORMATTED_DATA_DIR}/unformatted_data_gouv_datasets.json')

            formatted_datasets = self.format_datasets(datasets)
            
            # Enregistrement des données formatées
            self.save_json(formatted_datasets, f'{FORMATTED_DATA_DIR}/formatted_data_gouv_datasets.json')
            
            return formatted_datasets
        except requests.RequestException as e:
            logging.error(f"Request error while fetching datasets: {e}")
            return None

    def format_datasets(self, datasets: List[Dict]) -> List[Dict]:
        formatted_datasets = []
        for dataset in datasets:
            formatted_dataset = {
                "dataset_id": dataset["id"],
                "slug": dataset["slug"],
                "title": dataset["title"],
                "url": dataset["page"],
                "created_at": dataset.get("created_at", ""),
                "updated_at": dataset.get("last_update", ""),
                "discussions": dataset["metrics"]["discussions"],
                "followers": dataset["metrics"]["followers"],
                "resources_downloads": dataset["metrics"]["resources_downloads"],
                "reuses": dataset["metrics"]["reuses"],
                "views": dataset["metrics"]["views"],
                "source": "data_gouv"
            }
            formatted_datasets.append(formatted_dataset)
        return formatted_datasets


class DataEcoFetcher(BaseFetcher):
    def fetch_discussions(self) -> Optional[List[Dict]]:
        logging.info("Fetching discussions from data.economie.gouv.fr API :")
        all_data = []
        params = {
            "timezone": "UTC",
            "include_links": "false",
            "include_app_metas": "false",
            "limit": 100,
            "offset": 0
        }
        try:
            while True:
                response = requests.get(self.discussions_url, headers=HEADERS, params=params)
                response.raise_for_status()
                data_json = response.json()
                all_data.extend(data_json['results'])
                if len(data_json['results']) < params["limit"]:
                    break
                params["offset"] += params["limit"]
            logging.info(f"Fetched {len(all_data)} discussions from DataEco")

            # Enregistrement des données non formatées
            self.save_json(all_data, f'{UNFORMATTED_DATA_DIR}/unformatted_data_eco_discussions.json')

            formatted_discussions = self.format_discussions(all_data)
            
            # Enregistrement des données formatées
            self.save_json(formatted_discussions, f'{FORMATTED_DATA_DIR}/formatted_data_eco_discussions.json')
            
            return formatted_discussions
        except requests.RequestException as e:
            logging.error(f"Error fetching discussions: {e}")
            return None

    def format_discussions(self, discussions: List[Dict]) -> List[Dict]:
        formatted_discussions = []
        for discussion in discussions:
            formatted_discussion = {
                "jdd_id": discussion["id_jdd"],
                "discussion_id": discussion["id"],
                "parent_discussion_id": discussion["id_parent"],
                "title": discussion["sujet"],
                "pseudo": discussion["pseudo"],
                "comment": discussion["commentaire"],
                "created": discussion["horodatage"],
                "username": discussion["username"],
                "source": "data_eco"
            }
            formatted_discussions.append(formatted_discussion)
        return formatted_discussions

    def fetch_datasets(self) -> Optional[List[Dict]]:
        logging.info("Fetching datasets from data.economie.gouv.fr API :")
        all_data = []
        params = {
            "timezone": "UTC",
            "include_links": "false",
            "include_app_metas": "false",
            "limit": 100,
            "offset": 0
        }
        try:
            while True:
                response = requests.get(self.datasets_url, headers=HEADERS, params=params)
                response.raise_for_status()
                data = response.json()
                all_data.extend(data["results"])
                if len(data["results"]) < 100:
                    break
                params["offset"] += 100
            logging.info(f"Fetched {len(all_data)} datasets from DataEco")

            # Enregistrement des données non formatées
            self.save_json(all_data, f'{UNFORMATTED_DATA_DIR}/unformatted_data_eco_datasets.json')

            formatted_datasets = self.format_datasets(all_data)
            
            # Enregistrement des données formatées
            self.save_json(formatted_datasets, f'{FORMATTED_DATA_DIR}/formatted_data_eco_datasets.json')

            return formatted_datasets
        
        except requests.RequestException as e:
            logging.error(f"Error fetching datasets: {e}")
            return None

    def format_datasets(self, datasets: List[Dict]) -> List[Dict]:
        formatted_datasets = []
        for dataset in datasets:
            metas_default = dataset.get("metas", {}).get("default", {})
            metas_dcat = dataset.get("metas", {}).get("dcat", {})
            
            formatted_dataset = {
                "dataset_id": dataset.get("dataset_id"),
                "title": metas_default.get("title", "Unknown Title"),
                "publisher": metas_default.get("publisher", "Unknown Publisher"),
                "created_at": metas_dcat.get("created", "Unknown Created Date"),
                "updated_at": metas_default.get("modified", "Unknown Modified Date"),
                "source": "data_eco"
            }
            formatted_datasets.append(formatted_dataset)
        return formatted_datasets
