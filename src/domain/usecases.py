from src.domain.models import Message
from src.domain.gateways import AbstractCommentRepository
from src.infrastructure.services.api_fetcher_manager import APIFetcherManager
from typing import Dict


def create_message(repository: AbstractCommentRepository, discussion: Dict, dataset: Dict) -> Message:
    discussion_id = discussion.get("discussion_id") or discussion.get("message_id")
    print(f"Checking for existing message with discussion_id: {discussion_id}")
    existing_message = repository.get_message_by_sk(discussion_id)

    if existing_message:
        print(f"Duplicate message found for discussion_id: {discussion_id}")
        return existing_message

    # Récupération du titre du message
    title = discussion.get("title", "")
    parent_discussion_id = discussion.get("id_parent")

    # Si le titre est manquant et qu'un parent_discussion_id est fourni
    if not title and parent_discussion_id:
        parent_message = repository.get_message_by_sk(parent_discussion_id)
        if parent_message:
            title = parent_message.title
            print(f"Found parent title: {title}")
        else:
            print(f"Parent message not found for parent_discussion_id: {parent_discussion_id}")

    # Création du message
    message = Message.create(
        discussion_id,
        discussion.get("created") or discussion.get("date"),
        discussion.get("closed", False),
        discussion.get("dataset_id") or discussion.get("jdd_id"),
        title,  # Utiliser le titre récupéré ou le titre original
        discussion.get("first_message") or discussion.get("comment", ""),
        discussion.get("url_discussion", ""),
        discussion.get("source", ""),
        dataset.get("publisher", ""),
        dataset.get("created_at", ""),
        dataset.get("updated_at", ""),
        dataset.get("url", ""),
        parent_discussion_id,  # Passer le parent_discussion_id ici
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
        dataset_map = {dataset["dataset_id"]: dataset for dataset in datasets}
        if discussions:
            for discussion in discussions:
                dataset_id = discussion.get("dataset_id") or discussion.get("jdd_id")
                dataset = dataset_map.get(dataset_id, {})
                create_message(self.repository, discussion, dataset)
