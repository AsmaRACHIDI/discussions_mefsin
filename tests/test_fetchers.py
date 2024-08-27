import pytest
import json
from infrastructure.services.api_fetcher_manager import APIFetcherManager
from infrastructure.services.fetch_data import DataGouvFetcher
from infrastructure.services.fetch_data import DataEcoFetcher

@pytest.fixture
def fetcher_data_gouv():
    return APIFetcherManager.get_client('data_gouv')

@pytest.fixture
def fetcher_data_eco():
    return APIFetcherManager.get_client('data_eco')

# Unformatted_data
@pytest.fixture
def unformatted_datasets_data_gouv():
    return load_json_fixture('tests/fixtures/unformatted_data/unformatted_data_gouv_datasets.json')

@pytest.fixture
def unformatted_discussions_data_gouv():
    return load_json_fixture('tests/fixtures/unformatted_data/unformatted_data_gouv_discussions.json')

@pytest.fixture
def unformatted_datasets_data_eco():
    return load_json_fixture('tests/fixtures/unformatted_data/unformatted_data_eco_datasets.json')

@pytest.fixture
def unformatted_discussions_data_eco():
    return load_json_fixture('tests/fixtures/unformatted_data/unformatted_data_eco_discussions.json')

# Formatted_data
@pytest.fixture
def formatted_datasets_data_gouv():
    return load_json_fixture('tests/fixtures/formatted_data/formatted_data_gouv_datasets.json')

@pytest.fixture
def formatted_discussions_data_gouv():
    return load_json_fixture('tests/fixtures/formatted_data/formatted_data_gouv_discussions.json')

@pytest.fixture
def formatted_datasets_data_eco():
    return load_json_fixture('tests/fixtures/formatted_data/formatted_data_eco_datasets.json')

@pytest.fixture
def formatted_discussions_data_eco():
    return load_json_fixture('tests/fixtures/formatted_data/formatted_data_eco_discussions.json')


def load_json_fixture(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Fetch data
def test_fetch_discussions_data_gouv(fetcher_data_gouv):
    discussions = fetcher_data_gouv.fetch_discussions()
    
    print("Fetched discussions from data_gouv:")
    for discussion in discussions:
        print(discussion)

    assert len(discussions) > 0, "Expected to fetch at least one discussion"
    assert all('discussion_id' in discussion for discussion in discussions), "Each discussion should have a discussion_id"

def test_fetch_datasets_data_gouv(fetcher_data_gouv):
    datasets = fetcher_data_gouv.fetch_datasets()
    
    print("Fetched datasets from data_gouv:")
    for dataset in datasets:
        print(dataset)

    assert len(datasets) > 0, "Expected to fetch at least one dataset"
    assert all('dataset_id' in dataset for dataset in datasets), "Each dataset should have a dataset_id"

def test_fetch_discussions_data_eco(fetcher_data_eco):
    discussions = fetcher_data_eco.fetch_discussions()
    
    print("Fetched discussions from data_eco:")
    for discussion in discussions:
        print(discussion)

    assert len(discussions) > 0, "Expected to fetch at least one discussion"
    assert all('discussion_id' in discussion for discussion in discussions), "Each discussion should have a discussion_id"

def test_fetch_datasets_data_eco(fetcher_data_eco):
    datasets = fetcher_data_eco.fetch_datasets()
    
    print("Fetched datasets from data_eco:")
    for dataset in datasets:
        print(dataset)

    assert len(datasets) > 0, "Expected to fetch at least one dataset"
    assert all('dataset_id' in dataset for dataset in datasets), "Each dataset should have a dataset_id"

# Format data
def test_format_datasets_data_gouv(unformatted_datasets_data_gouv, formatted_datasets_data_gouv):
    fetcher = DataGouvFetcher(discussions_url="fake_discussions_url", datasets_url="fake_datasets_url") 
    # urls factices. Cela permet de satisfaire les arguments requis par les constructeurs sans dépendre de la configuration externe.
    formatted_datasets = fetcher.format_datasets(unformatted_datasets_data_gouv)
    assert formatted_datasets == formatted_datasets_data_gouv, f"Expected {formatted_datasets_data_gouv}, but got {formatted_datasets}"

def test_format_discussions_data_gouv(unformatted_discussions_data_gouv, formatted_discussions_data_gouv):
    fetcher = DataGouvFetcher(discussions_url="fake_discussions_url", datasets_url="fake_datasets_url")
    formatted_discussions = fetcher.format_discussions(unformatted_discussions_data_gouv)
    assert formatted_discussions == formatted_discussions_data_gouv, f"Expected {formatted_discussions_data_gouv}, but got {formatted_discussions}"

def test_format_datasets_data_eco(unformatted_datasets_data_eco, formatted_datasets_data_eco):
    fetcher = DataEcoFetcher(discussions_url="fake_discussions_url", datasets_url="fake_datasets_url")
    formatted_datasets = fetcher.format_datasets(unformatted_datasets_data_eco)
    assert formatted_datasets == formatted_datasets_data_eco, f"Expected {formatted_datasets_data_eco}, but got {formatted_datasets}"

def test_format_discussions_data_eco(unformatted_discussions_data_eco, formatted_discussions_data_eco):
    fetcher = DataEcoFetcher(discussions_url="fake_discussions_url", datasets_url="fake_datasets_url")
    formatted_discussions = fetcher.format_discussions(unformatted_discussions_data_eco)
    assert formatted_discussions == formatted_discussions_data_eco, f"Expected {formatted_discussions_data_eco}, but got {formatted_discussions}"
