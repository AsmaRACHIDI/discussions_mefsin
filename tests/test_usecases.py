# tests/test_fetchers.py
import pytest
import json
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from domain.models import Message
from infrastructure.repositories.tinydb_comment_repository import TinyDBCommentRepository
from domain.usecases import create_message, FetchAndStoreDiscussions
from typing import Dict


@pytest.fixture
def tinydb_repository():
    db = TinyDB(storage=MemoryStorage)
    repository = TinyDBCommentRepository()
    repository.db = db
    return repository

@pytest.fixture
def sample_data_gouv_discussion():
    with open('tests/fixtures/sample_data_gouv_discussions.json') as f:
        return json.load(f)[0]  # Charger le premier échantillon

@pytest.fixture
def sample_data_gouv_dataset():
    with open('tests/fixtures/sample_data_gouv_datasets.json') as f:
        return json.load(f)[0]  # Charger le premier échantillon

@pytest.fixture
def sample_data_eco_discussion():
    with open('tests/fixtures/sample_data_eco_discussions.json') as f:
        return json.load(f)[0]  # Charger le premier échantillon

@pytest.fixture
def sample_data_eco_dataset():
    with open('tests/fixtures/sample_data_eco_datasets.json') as f:
        return json.load(f)[0]  # Charger le premier échantillon

@pytest.fixture
def sample_message():
    return Message.create(
        discussion_id="sample_discussion",
        created="2024-01-01T00:00:00",
        closed=False,
        dataset_id="dataset_id",
        title="Title discussion",
        first_message="First message",
        url_discussion="http://example.com/discussion",
        source="data_gouv",
        dataset_title="Dataset Title",
        dataset_publisher="Sample Publisher",
        dataset_created_at="2024-01-01",
        dataset_updated_at="2024-01-02",
        dataset_url="http://example.com/dataset"
    )


def test_create_message(tinydb_repository, sample_data_gouv_discussion: Dict, sample_data_gouv_dataset: Dict):
    message = create_message(tinydb_repository, sample_data_gouv_discussion, sample_data_gouv_dataset)
    assert message.discussion_id == "sample_discussion"
    assert message.title == "Title discussion"
    assert message.dataset_title == "Dataset Title"
    assert tinydb_repository.get_message_by_sk("sample_discussion") is not None

def test_create_message_data_eco(tinydb_repository, sample_data_eco_discussion: Dict, sample_data_eco_dataset: Dict):
    message = create_message(tinydb_repository, sample_data_eco_discussion, sample_data_eco_dataset)
    assert message.discussion_id == "sample_discussion"
    assert message.title == "Title discussion"
    assert message.dataset_title == "Dataset Title"
    assert tinydb_repository.get_message_by_sk("sample_discussion") is not None


def test_get_message_by_id(tinydb_repository, sample_message):
    # Arrange
    tinydb_repository.create_message(sample_message)
    # Act
    retrieved_message = tinydb_repository.get_message_by_sk("sample_discussion")
    # Assert
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == "sample_discussion"
    assert retrieved_message.title == "Title discussion"


def test_get_message(tinydb_repository, sample_message: Message):
    # Arrange
    tinydb_repository.create_message(sample_message)
    # Act
    retrieved_message = tinydb_repository.get_message_by_sk(sample_message.discussion_id)
    # Assert
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == sample_message.discussion_id


def test_update_message(tinydb_repository, sample_message: Message):
    # Arrange
    tinydb_repository.create_message(sample_message)
    updated_message = sample_message.__dict__.copy()
    updated_message["first_message"] = "Updated message content"
    # Act
    tinydb_repository.update_message(sample_message.discussion_id, updated_message)
    # Assert
    retrieved_message = tinydb_repository.get_message_by_sk(sample_message.discussion_id)
    assert retrieved_message is not None
    assert retrieved_message.first_message == "Updated message content"


def test_delete_message(tinydb_repository, sample_message):
    # Arrange
    tinydb_repository.create_message(sample_message)
    # Act
    tinydb_repository.delete_message(sample_message.discussion_id)
    # Assert
    assert tinydb_repository.get_message_by_sk(sample_message.discussion_id) is None


def test_create_duplicate_message(tinydb_repository, sample_data_gouv_discussion, sample_data_gouv_dataset):
    # Act
    message1 = create_message(tinydb_repository, sample_data_gouv_discussion, sample_data_gouv_dataset)
    message2 = create_message(tinydb_repository, sample_data_gouv_discussion, sample_data_gouv_dataset)

    # Assert
    assert message1.discussion_id == message2.discussion_id
    messages = tinydb_repository.get_all_messages()
    assert len(messages) == 1


class MockFetcher:
        def __init__(self, discussions, datasets):
            self.discussions = discussions
            self.datasets = datasets

        def fetch_discussions(self):
            return self.discussions

        def fetch_datasets(self):
            return self.datasets
        

def test_fetch_and_store_discussions(tinydb_repository):
    # Arrange
    with open('tests/fixtures/sample_data_gouv_discussions.json') as f:
        sample_discussions = json.load(f)
    with open('tests/fixtures/sample_data_gouv_datasets.json') as f:
        sample_datasets = json.load(f)

    fetch_and_store = FetchAndStoreDiscussions(tinydb_repository, "mock")
    fetch_and_store.external_service = MockFetcher(sample_discussions, sample_datasets)

    # Act
    fetch_and_store.execute()

    # Assert
    for discussion in sample_discussions:
        stored_message = tinydb_repository.get_message_by_sk(discussion['id'])
        assert stored_message is not None
        assert stored_message.title == discussion['title']