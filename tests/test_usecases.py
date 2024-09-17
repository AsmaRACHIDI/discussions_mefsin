import pytest
import json
import os
import csv

from src.core.config import Config
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from src.domain import Message
from src.infrastructure.repositories.tinydb_comment_repository import TinyDBCommentRepository
from src.format import append_to_csv
from scripts.update_data import create_message, process_and_store_data
from unittest.mock import patch

import subprocess

SAMPLES_DATA_DIR = 'tests/fixtures/samples_data'

def ensure_samples_data():
    if not all(os.path.exists(os.path.join(SAMPLES_DATA_DIR, file)) for file in [
        'sample_data_gouv_discussions.json',
        'sample_data_gouv_datasets.json',
        'sample_data_eco_discussions.json',
        'sample_data_eco_datasets.json'
    ]):
        subprocess.run(['python', 'fetch_samples_data.py'], check=True)

@pytest.fixture(scope="session", autouse=True)
def setup_sample_data():
    ensure_samples_data()


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
    with open(filename, "r") as f:
        return json.load(f)


@pytest.fixture
def sample_discussions_data_gouv():
    return load_json_fixture("tests/fixtures/samples_data/sample_data_gouv_discussions.json")


@pytest.fixture
def sample_datasets_data_gouv():
    return load_json_fixture("tests/fixtures/samples_data/sample_data_gouv_datasets.json")


@pytest.fixture
def sample_discussions_data_eco():
    return load_json_fixture("tests/fixtures/samples_data/sample_data_eco_discussions.json")


@pytest.fixture
def sample_datasets_data_eco():
    return load_json_fixture("tests/fixtures/samples_data/sample_data_eco_datasets.json")


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
        source="data_gouv",
    )


def test_create_message_data_gouv(tinydb_repository, sample_discussions_data_gouv, sample_datasets_data_gouv):
    sample_discussion = sample_discussions_data_gouv[0]
    sample_dataset = sample_datasets_data_gouv[0]
    message = create_message(
        discussion=sample_discussion, dataset=sample_dataset, discussion_title=sample_discussion.get("title", "")
    )
    tinydb_repository.add_message(message)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_discussion["discussion_id"])
    assert retrieved_message is not None
    assert isinstance(message, Message)
    assert retrieved_message.discussion_id == sample_discussion["discussion_id"]
    assert retrieved_message.dataset_title == sample_dataset.get("title", "")


def test_create_message_data_eco(tinydb_repository, sample_discussions_data_eco, sample_datasets_data_eco):
    sample_discussion = sample_discussions_data_eco[0]
    sample_dataset = sample_datasets_data_eco[0]
    message = create_message(
        discussion=sample_discussion, dataset=sample_dataset, discussion_title=sample_discussion.get("title", "")
    )
    tinydb_repository.add_message(message)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_discussion["discussion_id"])
    assert retrieved_message is not None
    assert isinstance(message, Message)
    assert retrieved_message.discussion_id == sample_discussion["discussion_id"]
    assert retrieved_message.dataset_title == sample_dataset.get("title", "")


def test_get_message_by_id(tinydb_repository, sample_message):
    tinydb_repository.add_message(sample_message)
    retrieved_message = tinydb_repository.get_message_by_sk("sample_discussion")
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == "sample_discussion"
    assert retrieved_message.discussion_title == "Sample Title"


def test_get_message(tinydb_repository, sample_message):
    tinydb_repository.add_message(sample_message)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_message.discussion_id)
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == sample_message.discussion_id


def test_update_message(tinydb_repository, sample_message):
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
    message = create_message(
        discussion=sample_discussion, dataset=sample_dataset, discussion_title=sample_discussion.get("title", "")
    )
    tinydb_repository.add_message(message)
    tinydb_repository.add_message(message)  # Try adding the same message again
    messages = tinydb_repository.get_all_messages()
    assert len(messages) == 1, f"Expected 1 message, but found {len(messages)}"


@pytest.mark.parametrize(
    "api_type, sample_data",
    [
        ("data_gouv", "tests/fixtures/samples_data/sample_data_gouv_discussions.json"),
        ("data_eco", "tests/fixtures/samples_data/sample_data_eco_discussions.json"),
    ],
)
def test_process_and_store_data(tinydb_repository, api_type, sample_data):
    # Charger les données de l'échantillon pour l'API simulée
    with open(sample_data, "r") as f:
        sample_discussions_data = json.load(f)

    # Utiliser patch pour simuler les appels API
    with patch("infrastructure.services.api_fetcher_manager.APIFetcherManager.get_client") as mock_get_client:
        mock_fetcher = mock_get_client.return_value
        mock_fetcher.fetch_discussions.return_value = sample_discussions_data
        mock_fetcher.fetch_datasets.return_value = []

        # Exécuter la fonction de traitement et de stockage des données
        process_and_store_data(api_type)

        messages = tinydb_repository.get_all_messages()

        assert len(messages) > 0, "No messages were stored in the database"
        assert len(messages) == len(sample_discussions_data)


def test_json_to_csv_conversion(tinydb_repository, sample_discussions_data_gouv, sample_discussions_data_eco):
    # Ajouter 2 messages pour data_gouv et 2 messages pour data_eco
    for discussion in sample_discussions_data_gouv[:2] + sample_discussions_data_eco[:2]:
        message = create_message(discussion=discussion, dataset={}, discussion_title=discussion.get("title", ""))
        tinydb_repository.add_message(message)

    # Convertir les messages en JSON
    json_data = tinydb_repository.get_all_messages()
    json_data_dict = [message.to_dict() for message in json_data]
    assert isinstance(json_data_dict, list)
    assert all(isinstance(item, dict) for item in json_data_dict)

    # Chemin temporaire pour le fichier CSV de test
    test_csv_path = "tests/test_output.csv"
    append_to_csv(test_csv_path, json_data_dict)
    assert os.path.exists(test_csv_path), "Le fichier CSV n'a pas été créé."

    with open(test_csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        csv_data = list(reader)

    assert len(csv_data) == len(
        json_data_dict
    ), "Le nombre de lignes dans le fichier CSV ne correspond pas au nombre de dictionnaires JSON."
    assert all(
        any(item[key] == value for key, value in dict_data.items()) for item, dict_data in zip(csv_data, json_data_dict)
    )

    os.remove(test_csv_path)
