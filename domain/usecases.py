from domain.models import Message
from domain.gateways import AbstractCommentRepository
from infrastructure.services.api_fetcher_manager import APIFetcherManager
from typing import Dict

def create_message(repository: AbstractCommentRepository, discussion: Dict, dataset: Dict) -> Message:
    discussion_id = discussion.get("discussion_id") or discussion.get("message_id")
    print(f"Checking for existing message with discussion_id: {discussion_id}")
    existing_message = repository.get_message_by_sk(discussion_id)
    
    if existing_message:
        print(f"Duplicate message found for discussion_id: {discussion_id}")
        return existing_message
    
    print(f"No existing message found. Creating new message for discussion_id: {discussion_id}")
    message = Message.create(
        discussion_id,
        discussion.get("created") or discussion.get("date"),
        discussion.get("closed", False),
        discussion.get("dataset_id") or discussion.get("jdd_id"),
        discussion.get("title", ""),
        discussion.get("first_message") or discussion.get("comment", ""),
        discussion.get("url_discussion", ""),
        discussion.get("source", ""),
        dataset.get("title", ""),
        dataset.get("publisher", ""),
        dataset.get("created_at", ""),
        dataset.get("updated_at", ""),
        dataset.get("url", "")
    )
    
    repository.add_message(message)
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
