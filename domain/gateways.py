import abc
import json
from typing import List, Dict, Optional
from domain.models import Message


class AbstractCommentRepository(abc.ABC):
    @abc.abstractmethod
    def get_message_by_sk(self, discussion_id: str) -> Message:
        pass

    @abc.abstractmethod
    def add_message(self, message: Message) -> None:
        pass

    @abc.abstractmethod
    def update_message(self, discussion_id: str, updated_message: dict) -> None:
        pass

    @abc.abstractmethod
    def delete_message(self, discussion_id: str) -> None:
        pass

    @abc.abstractmethod
    def get_all_messages(self) -> List[Message]:
        pass


class BaseFetcher(abc.ABC):
    def __init__(self, discussions_url: str, datasets_url: str):
        self.discussions_url = discussions_url
        self.datasets_url = datasets_url

    @abc.abstractmethod
    def fetch_discussions(self) -> Optional[List[Dict]]:
        pass

    @abc.abstractmethod
    def fetch_datasets(self) -> Optional[List[Dict]]:
        pass

    @abc.abstractmethod
    def format_discussions(self, discussions: List[Dict]) -> List[Dict]:
        pass

    @abc.abstractmethod
    def format_datasets(self, datasets: List[Dict]) -> List[Dict]:
        pass

    def save_json(self, data: List[Dict], filepath: str):
        """Enregistre les données formatées dans un fichier JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

