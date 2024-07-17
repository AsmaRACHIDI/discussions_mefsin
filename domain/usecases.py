from typing import Dict
from domain.models import Message
from domain.gateways import AbstractCommentRepository
from infrastructure.services.api_fetcher_manager import APIFetcherManager


def create_message(repository: AbstractCommentRepository, discussion: Dict, dataset: Dict) -> Message:
    message = Message.create(
        discussion["discussion_id"], 
        discussion.get("created") or discussion.get("date"), 
        discussion.get("closed", False), 
        discussion.get("dataset_id") or discussion.get("jdd_id"), 
        discussion["title"], 
        discussion.get("first_message") or discussion.get("comment"), 
        discussion.get("url_discussion", ""), 
        discussion["source"],
        dataset["title"],
        dataset["publisher"],
        dataset["created_at"],
        dataset["updated_at"],
        dataset["url"]
    )
    repository.create_message(message)
    return message

class FetchAndStoreDiscussions:
    def __init__(self, repository: AbstractCommentRepository, api_type: str):
        self.repository = repository
        self.external_service = APIFetcherManager.get_client(api_type)

    def execute(self):
        discussions = self.external_service.fetch_discussions()
        datasets = self.external_service.fetch_datasets()
        dataset_map = {dataset['dataset_id']: dataset for dataset in datasets}
        if discussions:
            for discussion in discussions:
                dataset_id = discussion.get("dataset_id") or discussion.get("jdd_id")
                dataset = dataset_map.get(dataset_id, {})
                create_message(self.repository, discussion, dataset)
