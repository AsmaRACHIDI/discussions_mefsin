import pytest
import json
import os
from core.config import Config
from tinydb import TinyDB
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
    repository.clear_db()  # Clear the database before each test
    # Chaque test appelle cette méthode pour s'assurer que la base de données est vide avant l'exécution du test.
    yield repository # l'argument "yield" permet au lieu de return d'executer du code après que le test soit terminé
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

def test_create_message_data_gouv(tinydb_repository, sample_discussions_data_gouv: Dict, sample_datasets_data_gouv: Dict):
    sample_discussion = sample_discussions_data_gouv[0]
    sample_dataset = sample_datasets_data_gouv[0]
    message = create_message(tinydb_repository, sample_discussion, sample_dataset)
    assert message.discussion_id == sample_discussion.get('discussion_id') or sample_discussion.get('message_id')
    assert message.dataset_title == sample_dataset.get('title', "")
    assert tinydb_repository.get_message_by_sk(sample_discussion.get('discussion_id') or sample_discussion.get('message_id')) is not None

def test_create_message_data_eco(tinydb_repository, sample_discussions_data_eco: Dict, sample_datasets_data_eco: Dict):
    sample_discussion = sample_discussions_data_eco[0]
    sample_dataset = sample_datasets_data_eco[0]
    message = create_message(tinydb_repository, sample_discussion, sample_dataset)
    assert message.discussion_id == sample_discussion.get('discussion_id') or sample_discussion.get('message_id')
    assert message.dataset_title == sample_dataset.get('title', "")
    assert tinydb_repository.get_message_by_sk(sample_discussion.get('discussion_id') or sample_discussion.get('message_id')) is not None

def test_get_message_by_id(tinydb_repository, sample_message):
    #create_message(tinydb_repository, sample_message.__dict__, sample_message.__dict__)
    tinydb_repository.add_message(sample_message)
    retrieved_message = tinydb_repository.get_message_by_sk("sample_discussion")
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == "sample_discussion"
    assert retrieved_message.title == "Sample Title"

def test_get_message(tinydb_repository, sample_message: Message):
    tinydb_repository.add_message(sample_message)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_message.discussion_id)
    assert retrieved_message is not None
    assert retrieved_message.discussion_id == sample_message.discussion_id

def test_update_message(tinydb_repository, sample_message: Message):
    tinydb_repository.add_message(sample_message)
    updated_fields = {"first_message": "Updated message content"}
    tinydb_repository.update_message(sample_message.discussion_id, updated_fields)
    retrieved_message = tinydb_repository.get_message_by_sk(sample_message.discussion_id)
    assert retrieved_message is not None
    assert retrieved_message.first_message == "Updated message content"

def test_delete_message(tinydb_repository, sample_message):
    tinydb_repository.add_message(sample_message)
    tinydb_repository.delete_message(sample_message.discussion_id)
    assert tinydb_repository.get_message_by_sk(sample_message.discussion_id) is None

def test_create_duplicate_message(tinydb_repository, sample_discussions_data_gouv, sample_datasets_data_gouv):
    tinydb_repository.clear_db()  # Clear the database before the test
    sample_discussion = sample_discussions_data_gouv[0]
    sample_dataset = sample_datasets_data_gouv[0]
    message1 = create_message(tinydb_repository, sample_discussion, sample_dataset)
    message2 = create_message(tinydb_repository, sample_discussion, sample_dataset)
    
    assert message1.discussion_id == message2.discussion_id
    messages = tinydb_repository.get_all_messages()
    
    print("Messages in DB after attempting to create duplicate:")
    for msg in messages:
        print(f"Discussion ID: {msg.discussion_id}, Title: {msg.title}")

    assert len(messages) == 1, f"Expected 1 message, but found {len(messages)}"

def test_fetch_and_store_discussions(tinydb_repository, sample_discussions_data_gouv, sample_datasets_data_gouv):
    tinydb_repository.clear_db()  # Clear the database before the test
    fetch_and_store = FetchAndStoreDiscussions(repository=tinydb_repository, api_type="data_gouv")
    fetch_and_store.external_service.fetch_discussions = lambda: sample_discussions_data_gouv
    fetch_and_store.external_service.fetch_datasets = lambda: sample_datasets_data_gouv
    fetch_and_store.execute()
    
    messages = tinydb_repository.get_all_messages()
    
    print("Messages in DB after fetching and storing discussions:")
    for msg in messages:
        print(f"Discussion ID: {msg.discussion_id}, Title: {msg.title}")

    assert len(messages) == 2, f"Expected 2 messages, but found {len(messages)}"
    assert messages[0].discussion_id == sample_discussions_data_gouv[0].get('discussion_id') or sample_discussions_data_gouv[0].get('message_id')
    assert messages[1].discussion_id == sample_discussions_data_gouv[1].get('discussion_id') or sample_discussions_data_gouv[1].get('message_id')
