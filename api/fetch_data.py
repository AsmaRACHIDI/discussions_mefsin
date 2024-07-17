# api/fetch_data.py
import requests
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from core.config import Config


HEADERS = {"Authorization": f"Apikey {Config.API_KEY}"}


class BaseFetcher(ABC):
    def __init__(self, discussions_url: str, datasets_url: str):
        self.discussions_url = discussions_url
        self.datasets_url = datasets_url

    @abstractmethod
    def fetch_discussions(self) -> Optional[List[Dict]]:
        pass

    @abstractmethod
    def fetch_datasets(self) -> Optional[List[Dict]]:
        pass

    @abstractmethod
    def format_discussions(self, discussions: List[Dict]) -> List[Dict]:
        pass

    @abstractmethod
    def format_datasets(self, datasets: List[Dict]) -> List[Dict]:
        pass


class DataGouvFetcher(BaseFetcher):
    def fetch_discussions(self) -> Optional[List[Dict]]:
        try:
            response = requests.get(self.discussions_url)
            response.raise_for_status()
            data_json = response.json()
            logging.info("Discussions from data.gouv.fr fetched successfully!")
            return self.format_discussions(data_json)
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
        datasets = []
        page = 1
        while True:
            url = f"{self.datasets_url}?page={page}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if not data["data"]:
                break
            datasets.extend(data["data"])
            page += 1
        return self.format_datasets(datasets)

    def format_datasets(self, datasets: List[Dict]) -> List[Dict]:
        formatted_datasets = []
        for dataset in datasets:
            formatted_dataset = {
                "dataset_id": dataset["id"],
                "slug": dataset["slug"],
                "title": dataset["title"],
                "url": dataset["page"],
                "source": "data_gouv",
                "publisher": dataset.get("publisher", "Unknown"),
                "created_at": dataset.get("created_at", ""),
                "updated_at": dataset.get("updated_at", "")
            }
            formatted_datasets.append(formatted_dataset)
        return formatted_datasets

class DataEcoFetcher(BaseFetcher):
    def fetch_discussions(self) -> Optional[List[Dict]]:
        all_data = []
        limit = 100
        offset = 0
        try:
            while True:
                response = requests.get(self.discussions_url, headers=HEADERS, params={"limit": limit, "offset": offset})
                response.raise_for_status()
                data_json = response.json()
                all_data.extend(data_json['results'])
                if len(data_json['results']) < limit:
                    break
                offset += limit
            return self.format_discussions(all_data)
        except requests.RequestException as e:
            logging.error(f"HTTP error occurred: {e}")
            return None

    def format_discussions(self, discussions: List[Dict]) -> List[Dict]:
        formatted_discussions = []
        for discussion in discussions:
            formatted_discussion = {
                "jdd_id": discussion["id_jdd"],
                "message_id": discussion["id"],
                "parent_message_id": discussion["id_parent"],
                "title": discussion["sujet"],
                "pseudo": discussion["pseudo"],
                "comment": discussion["commentaire"],
                "date": discussion["horodatage"],
                "username": discussion["username"],
                "source": "data_eco"
            }
            formatted_discussions.append(formatted_discussion)
        return formatted_discussions

    def fetch_datasets(self) -> Optional[List[Dict]]:
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
            return self.format_datasets(all_data)
        except requests.RequestException as e:
            logging.error(f"Error fetching datasets: {e}")
            return None

    def format_datasets(self, datasets: List[Dict]) -> List[Dict]:
        formatted_datasets = []
        for dataset in datasets:
            formatted_dataset = {
                "dataset_id": dataset["dataset_id"],
                "title": dataset["metas"]["default"]["title"],
                "publisher": dataset["metas"]["default"]["publisher"],
                "created_at": dataset["metas"]["dcat"]["created"],
                "updated_at": dataset["metas"]["default"]["modified"],
                "source": "data_eco"
            }
            formatted_datasets.append(formatted_dataset)
        return formatted_datasets
