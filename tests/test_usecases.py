import pytest
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from domain.models import Message
from infrastructure.repositories.tinydb_discussions_repository import TinyDBCommentRepository
from domain.usecases import create_message, FetchAndStoreDiscussions
from typing import Dict


@pytest.fixture
def tinydb_repository():
    db = TinyDB(storage=MemoryStorage)
    repository = TinyDBCommentRepository()
    repository.db = db
    return repository

@pytest.fixture
def sample_discussion():
    return {
        "discussion_id": "sample_discussion",
        "created": "2023-01-01T00:00:00",
        "closed": False,
        "dataset_id": "dataset_id",
        "title": "Title discussion",
        "first_message": "This is the first message",
        "url_discussion": "http://example.com/discussion",
        "source": "data_gouv"
    }

@pytest.fixture
def sample_dataset():
    return {
        "dataset_id": "sample_dataset",
        "title": "Dataset",
        "publisher": "Publisher",
        "created_at": "2023-01-01",
        "updated_at": "2023-01-02",
        "url": "http://example.com/dataset"
    }

@pytest.fixture
def sample_message():
    return Message.create(
        discussion_id="sample_discussion",
        created="2023-01-01T00:00:00",
        closed=False,
        dataset_id="sample_dataset",
        title="Sample Title",
        first_message="This is a sample first message",
        url_discussion="http://example.com/discussion",
        source="data_gouv",
        dataset_title="Sample Dataset",
        dataset_publisher="Sample Publisher",
        dataset_created_at="2023-01-01",
        dataset_updated_at="2023-01-02",
        dataset_url="http://example.com/dataset"
    )


def test_create_message(tinydb_repository, sample_discussion: Dict, sample_dataset: Dict):
    message = create_message(tinydb_repository, sample_discussion, sample_dataset)
    assert message.discussion_id == "sample_discussion"
    assert message.title == "Title discussion"
    assert message.dataset_title == "Dataset"
    assert tinydb_repository.get_message_by_sk("sample_discussion") is not None


def test_get_message_by_id(tinydb_repository, sample_message):
    # Arrange
    tinydb_repository.create_message(sample_message)
    # Act
    retrieved_message = tinydb_repository.get_message_by_sk("sample_discussion")
    # Assert
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == "sample_discussion"
    assert retrieved_message.title == "Sample Title"


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
    updated_message = sample_message
    updated_message.first_message = "Updated message content"
    # Act
    tinydb_repository.create_message(updated_message) 
    # Assert
    retrieved_message = tinydb_repository.get_message_by_sk(updated_message.discussion_id)
    assert retrieved_message is not None
    assert retrieved_message.first_message == "Updated message content"


def test_delete_message(tinydb_repository, sample_message):
    # Arrange
    tinydb_repository.create_message(sample_message) 
    # Act
    tinydb_repository.delete_message(sample_message.discussion_id) 
    # Assert
    assert tinydb_repository.get_message_by_sk(sample_message.discussion_id) is None
