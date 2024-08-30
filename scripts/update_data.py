import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.services.api_fetcher_manager import APIFetcherManager
from domain.models import Message
from infrastructure.repositories.tinydb_comment_repository import TinyDBCommentRepository
from src.format import dump_json
from inference.inference_script import annotate_a_message


def fetch_and_format_data(api_type):
    fetcher = APIFetcherManager.get_client(api_type)
    
    discussions = fetcher.fetch_discussions()
    if discussions is None:
        print(f"Failed to fetch discussions from {api_type}")
        return [], {}
    
    datasets = fetcher.fetch_datasets()
    if datasets is None:
        print(f"Failed to fetch datasets from {api_type}")
        return [], {}

    # Map datasets by ID
    dataset_map = {dataset['dataset_id']: dataset for dataset in datasets}
    
    return discussions, dataset_map


def create_message(discussion, dataset, discussion_title):
    return Message.create(
        discussion_id=discussion["discussion_id"],
        discussion_created=discussion.get("created", ""),
        discussion_closed=discussion.get("closed", ""),
        dataset_id=dataset.get("dataset_id", ""),
        parent_discussion_id=discussion.get("parent_discussion_id", ""),
        discussion_title=discussion_title, 
        comment=discussion.get("first_message") or discussion.get("comment", ""),
        url_discussion=discussion.get("url_discussion", ""),
        dataset_title=dataset.get("title"),
        dataset_publisher=dataset.get("publisher", ""),
        dataset_created_at=dataset.get("created_at", ""),
        dataset_updated_at=dataset.get("updated_at", ""),
        dataset_url=dataset.get("url", ""),
        source=discussion.get("source", "")
    )


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

        discussion_title = discussion.get("title", "")

        if api_type == "data_eco" and discussion.get("parent_discussion_id"):
            parent_discussion_id = discussion["parent_discussion_id"]
            parent_discussion = discussion_map.get(parent_discussion_id, {})
            if parent_discussion:
                discussion_title = parent_discussion.get("title", discussion_title)

        message = create_message(discussion, dataset, discussion_title)
        repository.add_message(message)

    print(f"Finished processing discussions from {api_type}")


def infer_and_update_messages():
    repository = TinyDBCommentRepository()
    
    messages = repository.get_all_messages()

    total_messages = len(messages)
    annotated_messages = 0

    for message in messages:
        if not message.prediction_motif or not message.prediction_sous_motif:
            prediction_motif, prediction_sous_motif = annotate_a_message(
                message.discussion_title,
                message.comment
            )
            # Préparez le dictionnaire de mise à jour
            updated_message = {
                "prediction_motif": prediction_motif,
                "prediction_sous_motif": prediction_sous_motif
            }
            # Appelez la méthode update_message avec les bons arguments
            repository.update_message(message.discussion_id, updated_message)
            
            annotated_messages += 1  # Incrémentez le compteur des messages annotés
            print(f"\n{annotated_messages} messages annotés / {total_messages} messages")
    
    print(f"Inference and update of messages completed.")


def save_json_data(repository, output_path):
    json_data = repository.get_all_messages()
    json_data_dict = [message.to_dict() for message in json_data]
    dump_json(output_path, json_data_dict)
    print(f"JSON data saved to {output_path}")


def main():
    repository = TinyDBCommentRepository()

    process_and_store_data("data_gouv")
    process_and_store_data("data_eco")

    infer_and_update_messages()

    json_output_path = "app/static/data/test.json"
    save_json_data(repository, json_output_path)

if __name__ == "__main__":
    main()
