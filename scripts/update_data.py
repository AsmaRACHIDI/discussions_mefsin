import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.services.api_fetcher_manager import APIFetcherManager
from domain.models import Message
from infrastructure.repositories.tinydb_comment_repository import TinyDBCommentRepository
from src.format import dump_json


def fetch_and_format_data(api_type):
    fetcher = APIFetcherManager.get_client(api_type)
    
    # Fetch discussions
    discussions = fetcher.fetch_discussions()
    if discussions is None:
        print(f"Failed to fetch discussions from {api_type}")
        return [], {}
    
    # Fetch datasets
    datasets = fetcher.fetch_datasets()
    if datasets is None:
        print(f"Failed to fetch datasets from {api_type}")
        return [], {}

    # Map datasets by ID
    dataset_map = {dataset['dataset_id']: dataset for dataset in datasets}
    
    return discussions, dataset_map

def process_and_store_data(api_type):
    repository = TinyDBCommentRepository()

    # Fetch and format data
    discussions, dataset_map = fetch_and_format_data(api_type)
    
    if not discussions:
        print(f"No discussions to process from {api_type}")
        return
    
    # Pour mapper parent_discussion_id et le title du discussion_id correspondant
    discussion_map = {discussion['discussion_id']: discussion for discussion in discussions}
    
    for discussion in discussions:
        dataset_id = discussion.get("dataset_id") or discussion.get("jdd_id")
        dataset = dataset_map.get(dataset_id, {})

        # Determine the title of the discussion
        if api_type == "data_eco" and "parent_discussion_id" in discussion:
            # If there's a parent discussion, get its title
            parent_discussion_id = discussion["parent_discussion_id"]
            parent_discussion = discussion_map.get(parent_discussion_id, {})
            discussion_title = parent_discussion.get("title", "")
        else:
            # Otherwise, use the current discussion's title
            discussion_title = discussion.get("title", "")

        # Create a Message object from the discussion and dataset data
        message = Message.create(
            discussion_id=discussion["discussion_id"],
            discussion_created = discussion.get("created", ""),
            discussion_closed=discussion.get("closed", ""),
            dataset_id=dataset_id,
            parent_discussion_id=discussion.get("parent_discussion_id", ""),
            discussion_title=discussion_title, # Ajouter title du parent_id dans le cas de data_eco
            comment=discussion.get("first_message") or discussion.get("comment", ""),
            url_discussion=discussion.get("url_discussion", ""),
            dataset_title=dataset.get("title", ""),
            dataset_publisher=dataset.get("publisher", ""),
            dataset_created_at=dataset.get("created_at", ""),
            dataset_updated_at=dataset.get("updated_at", ""),
            dataset_url=dataset.get("url", ""),
            source=discussion["source"]
        )

        # Add the message to the repository (duplicates will be handled by add_message)
        repository.add_message(message)
        print(f"Processed message with ID {message.discussion_id} from {api_type}.")

    print(f"Finished processing discussions from {api_type}")

def main():
    repository = TinyDBCommentRepository()

    # Process data from both sources
    process_and_store_data("data_gouv")
    process_and_store_data("data_eco")

    # Récupération des données JSON depuis le repository
    json_data = repository.get_all_messages()
    
    # Convertir json_data en liste de dictionnaires
    json_data_dict = [message.to_dict() for message in json_data]
    print("Type de json_data_dict:", type(json_data_dict))

    # Sauvegarder dans un fichier JSON
    json_output_path = "app/static/data/test.json"
    dump_json(json_output_path, json_data_dict)
    print(f"JSON data saved to {json_output_path}")

if __name__ == "__main__":
    main()
