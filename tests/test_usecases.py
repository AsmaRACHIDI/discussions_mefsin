import pytest
import json
import os
import csv

from core.config import Config
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from domain.models import Message
from infrastructure.repositories.tinydb_comment_repository import TinyDBCommentRepository
from src.format import append_to_csv, dump_json
from domain.usecases import FetchAndStoreDiscussions
from typing import Dict

@pytest.fixture
def tinydb_repository():
    db = TinyDB(storage=MemoryStorage)
    repository = TinyDBCommentRepository()
    repository.db = db
    repository.clear_db()  # Clear the database before each test
    yield repository
    repository.clear_db()  # Clear the database after each test
    if os.path.exists(Config.TINYDB_PATH):
        os.remove(Config.TINYDB_PATH)  # Remove the JSON file after each test

def load_json_fixture(filename):
    with open(filename, 'r') as f:
        return json.load(f)

@pytest.fixture
def sample_discussions_data_gouv():
    return load_json_fixture('tests/fixtures/samples_data/sample_data_gouv_discussions.json')

@pytest.fixture
def sample_datasets_data_gouv():
    return load_json_fixture('tests/fixtures/samples_data/sample_data_gouv_datasets.json')

@pytest.fixture
def sample_discussions_data_eco():
    return load_json_fixture('tests/fixtures/samples_data/sample_data_eco_discussions.json')

@pytest.fixture
def sample_datasets_data_eco():
    return load_json_fixture('tests/fixtures/samples_data/sample_data_eco_datasets.json')

@pytest.fixture
def sample_message():
    return Message.create(
        discussion_id="sample_discussion",
        discussion_created="2023-01-01T00:00:00",
        discussion_closed=False,
        dataset_id="sample_dataset",
        parent_discussion_id="",
        discussion_title="Sample Title",
        comment="This is a sample first message",
        url_discussion="http://example.com/discussion",
        dataset_title="Sample Dataset",
        dataset_publisher="Sample Publisher",
        dataset_created_at="2023-01-01",
        dataset_updated_at="2023-01-02",
        dataset_url="http://example.com/dataset",
        source="data_gouv"
    )


def test_create_message_data_gouv(tinydb_repository, sample_discussions_data_gouv: Dict, sample_datasets_data_gouv: Dict):
    sample_discussion = sample_discussions_data_gouv[0]
    sample_dataset = sample_datasets_data_gouv[0]
    message = Message.create(
        discussion_id=sample_discussion["discussion_id"],
        discussion_created=sample_discussion.get("created", ""),
        discussion_closed=sample_discussion.get("closed", ""),
        dataset_id=sample_dataset.get("dataset_id", ""),
        parent_discussion_id=sample_discussion.get("parent_discussion_id", ""),
        discussion_title=sample_discussion.get("title", ""),
        comment=sample_discussion.get("first_message", ""),
        url_discussion=sample_discussion.get("url_discussion", ""),
        dataset_title=sample_dataset.get("title", ""),
        dataset_publisher=sample_dataset.get("publisher", ""),
        dataset_created_at=sample_dataset.get("created_at", ""),
        dataset_updated_at=sample_dataset.get("updated_at", ""),
        dataset_url=sample_dataset.get("url", ""),
        source=sample_discussion.get("source", "")
    )
    tinydb_repository.add_message(message)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_discussion["discussion_id"])
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == sample_discussion["discussion_id"]
    assert retrieved_message.dataset_title == sample_dataset.get('title', "")


def test_create_message_data_eco(tinydb_repository, sample_discussions_data_eco: Dict, sample_datasets_data_eco: Dict):
    sample_discussion = sample_discussions_data_eco[0]
    sample_dataset = sample_datasets_data_eco[0]
    message = Message.create(
        discussion_id=sample_discussion["discussion_id"],
        discussion_created=sample_discussion.get("created", ""),
        discussion_closed=sample_discussion.get("closed", ""),
        dataset_id=sample_dataset.get("dataset_id", ""),
        parent_discussion_id=sample_discussion.get("parent_discussion_id", ""),
        discussion_title=sample_discussion.get("title", ""),
        comment=sample_discussion.get("first_message", ""),
        url_discussion=sample_discussion.get("url_discussion", ""),
        dataset_title=sample_dataset.get("title", ""),
        dataset_publisher=sample_dataset.get("publisher", ""),
        dataset_created_at=sample_dataset.get("created_at", ""),
        dataset_updated_at=sample_dataset.get("updated_at", ""),
        dataset_url=sample_dataset.get("url", ""),
        source=sample_discussion.get("source", "")
    )
    tinydb_repository.add_message(message)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_discussion["discussion_id"])
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == sample_discussion["discussion_id"]
    assert retrieved_message.dataset_title == sample_dataset.get('title', "")


def test_get_message_by_id(tinydb_repository, sample_message):
    tinydb_repository.add_message(sample_message)
    retrieved_message = tinydb_repository.get_message_by_sk("sample_discussion")
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == "sample_discussion"
    assert retrieved_message.discussion_title == "Sample Title"


def test_get_message(tinydb_repository, sample_message: Message):
    tinydb_repository.add_message(sample_message)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_message.discussion_id)
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == sample_message.discussion_id


def test_update_message(tinydb_repository, sample_message: Message):
    tinydb_repository.add_message(sample_message)
    updated_fields = {"comment": "Updated message content"}
    tinydb_repository.update_message(sample_message.discussion_id, updated_fields)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_message.discussion_id)
    assert retrieved_message is not None
    assert retrieved_message.comment == "Updated message content"


def test_delete_message(tinydb_repository, sample_message):
    tinydb_repository.add_message(sample_message)
    tinydb_repository.delete_message(sample_message.discussion_id)
    assert tinydb_repository.get_message_by_sk(sample_message.discussion_id) is None


def test_create_duplicate_message(tinydb_repository, sample_discussions_data_gouv, sample_datasets_data_gouv):
    tinydb_repository.clear_db()
    sample_discussion = sample_discussions_data_gouv[0]
    sample_dataset = sample_datasets_data_gouv[0]
    message1 = Message.create(
        discussion_id=sample_discussion["discussion_id"],
        discussion_created=sample_discussion.get("created", ""),
        discussion_closed=sample_discussion.get("closed", ""),
        dataset_id=sample_dataset.get("dataset_id", ""),
        parent_discussion_id=sample_discussion.get("parent_discussion_id", ""),
        discussion_title=sample_discussion.get("title", ""),
        comment=sample_discussion.get("first_message", ""),
        url_discussion=sample_discussion.get("url_discussion", ""),
        dataset_title=sample_dataset.get("title", ""),
        dataset_publisher=sample_dataset.get("publisher", ""),
        dataset_created_at=sample_dataset.get("created_at", ""),
        dataset_updated_at=sample_dataset.get("updated_at", ""),
        dataset_url=sample_dataset.get("url", ""),
        source=sample_discussion.get("source", "")
    )
    message2 = Message.create(
        discussion_id=sample_discussion["discussion_id"],
        discussion_created=sample_discussion.get("created", ""),
        discussion_closed=sample_discussion.get("closed", ""),
        dataset_id=sample_dataset.get("dataset_id", ""),
        parent_discussion_id=sample_discussion.get("parent_discussion_id", ""),
        discussion_title=sample_discussion.get("title", ""),
        comment=sample_discussion.get("first_message", ""),
        url_discussion=sample_discussion.get("url_discussion", ""),
        dataset_title=sample_dataset.get("title", ""),
        dataset_publisher=sample_dataset.get("publisher", ""),
        dataset_created_at=sample_discussion.get("created_at", ""),
        dataset_updated_at=sample_discussion.get("updated_at", ""),
        dataset_url=sample_discussion.get("url", ""),
        source=sample_discussion.get("source", "")
    )
    tinydb_repository.add_message(message1)
    tinydb_repository.add_message(message2)

    messages = tinydb_repository.get_all_messages()

    print("Messages in DB after attempting to create duplicate:")
    for msg in messages:
        print(f"Discussion ID: {msg.discussion_id}, Discussion Title: {msg.discussion_title}")

    assert len(messages) == 1, f"Expected 1 message, but found {len(messages)}"


def test_fetch_and_store_discussions(tinydb_repository, sample_discussions_data_gouv, sample_datasets_data_gouv):
    tinydb_repository.clear_db()
    fetch_and_store = FetchAndStoreDiscussions(repository=tinydb_repository, api_type="data_gouv")
    fetch_and_store.external_service.fetch_discussions = lambda: sample_discussions_data_gouv
    fetch_and_store.external_service.fetch_datasets = lambda: sample_datasets_data_gouv
    fetch_and_store.execute()

    messages = tinydb_repository.get_all_messages()

    print("Messages in DB after fetching and storing discussions:")
    for msg in messages:
        print(f"Discussion ID: {msg.discussion_id}, Discussion Title: {msg.discussion_title}")

    # Assertions based on your test requirements
    assert len(messages) > 0, "No messages found in DB"


def test_json_to_csv_conversion(tinydb_repository, sample_discussions_data_gouv, sample_discussions_data_eco):
    # Ajouter 2 messages pour data_gouv et 2 messages pour data_eco
    for data in [sample_discussions_data_gouv[:2], sample_discussions_data_eco[:2]]:
        for discussion in data:
            message = Message.create(
                discussion_id=discussion["discussion_id"],
                discussion_created=discussion.get("created", ""),
                discussion_closed=discussion.get("closed", ""),
                dataset_id=discussion.get("dataset_id", ""),
                parent_discussion_id=discussion.get("parent_discussion_id", ""),
                discussion_title=discussion.get("title", ""),
                comment=discussion.get("first_message", ""),
                url_discussion=discussion.get("url_discussion", ""),
                dataset_title=discussion.get("dataset_title", ""),
                dataset_publisher=discussion.get("dataset_publisher", ""),
                dataset_created_at=discussion.get("dataset_created_at", ""),
                dataset_updated_at=discussion.get("dataset_updated_at", ""),
                dataset_url=discussion.get("dataset_url", ""),
                source=discussion.get("source", "")
            )
            tinydb_repository.add_message(message)
    
    # Convertir les messages en JSON
    json_data = tinydb_repository.get_all_messages()
    json_data_dict = [message.to_dict() for message in json_data]

    # Vérifier que json_data_dict est une liste de dictionnaires
    assert isinstance(json_data_dict, list)
    assert all(isinstance(item, dict) for item in json_data_dict)

    # Chemin temporaire pour le fichier CSV de test
    test_csv_path = "tests/test_output.csv"
    
    # Appeler la fonction append_to_csv
    append_to_csv(test_csv_path, json_data_dict)
    
    # Vérifier que le fichier CSV a été créé et n'est pas vide
    assert os.path.exists(test_csv_path), "Le fichier CSV n'a pas été créé."
    
    with open(test_csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        csv_data = list(reader)
    
    # Vérifier que le CSV contient les données correctes
    assert len(csv_data) == len(json_data_dict), "Le nombre de lignes dans le fichier CSV ne correspond pas au nombre de dictionnaires JSON."
    assert all(any(item[key] == value for key, value in dict_data.items()) for item, dict_data in zip(csv_data, json_data_dict))
    
    # Nettoyer le fichier après le test
    os.remove(test_csv_path)
