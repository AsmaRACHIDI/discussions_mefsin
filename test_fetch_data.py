import pytest
import os
import csv

from dotenv import load_dotenv
from fetch_data import fetch_discussions_from_data_gouv_api, fetch_datasets_from_data_eco_api, fetch_discussions_from_data_eco_api, format_data, save_to_csv

# Récupération des variables d'environnement
load_dotenv()

@pytest.fixture
def data_gouv_api_url():
    return "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"

@pytest.fixture
def data_eco_datasets_api_url():
    return "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"

@pytest.fixture
def data_eco_discussions_api_url():
    return "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/interne-discussions/records"


# def test_fetch_data_from_data_gouv_api(data_gouv_api_url):
    # data = fetch_data_from_data_gouv_api(data_gouv_api_url)
def test_fetch_discussions_from_data_gouv_api():
    data = fetch_discussions_from_data_gouv_api()
    assert isinstance(data, list)
    assert len(data) > 0


#def test_fetch_data_from_data_eco_api(data_eco_api_url):
    #data = fetch_data_from_data_eco_api(data_eco_api_url)
def test_fetch_datasets_from_data_eco_api():
    data = fetch_datasets_from_data_eco_api()
    assert isinstance(data, list)
    assert len(data) > 0



def test_fetch_discussions_from_data_eco_api():
    data = fetch_discussions_from_data_eco_api()
    assert isinstance(data, dict)
    assert "records" in data
    assert "total_count" in data
    assert len(data["records"]) == data["total_count"]
    print(len(data["records"]))


def test_format_data_gouv_discussions():
    sample_data = [
        {
            "id": "1",
            "created": "2023-01-01T00:00:00Z",
            "closed": "2023-01-02T00:00:00Z",
            "subject": {"id": "dataset_1"},
            "title": "Discussion 1",
            "discussion": [{"content": "First message"}],
            "url": "http://example.com/discussion/1"
        },
        {
            "id": "2",
            "created": "2023-01-03T00:00:00Z",
            "closed": "2023-01-04T00:00:00Z",
            "subject": {"id": "dataset_2"},
            "title": "Discussion 2",
            "discussion": [{"content": "First message"}],
            "url": "http://example.com/discussion/2"
        }
    ]
    formatted_data = format_data(sample_data, "data_gouv_discussions")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == 2
    for discussion in formatted_data:
        assert "id" in discussion
        assert "created" in discussion
        assert "closed" in discussion
        assert "dataset_id" in discussion
        assert "title" in discussion
        assert "first_message" in discussion
        assert "url_discussion" in discussion


def test_format_data_eco_datasets():
    sample_data = [
        {
            "dataset_id": "1",
            "metas": {
                "default": {
                    "title": "Dataset 1",
                    "publisher": "Publisher 1",
                    "modified": "2023-01-02T00:00:00Z"
                },
                "dcat": {
                    "created": "2023-01-01T00:00:00Z"
                }
            }
        },
        {
            "dataset_id": "2",
            "metas": {
                "default": {
                    "title": "Dataset 2",
                    "publisher": "Publisher 2",
                    "modified": "2023-01-04T00:00:00Z"
                },
                "dcat": {
                    "created": "2023-01-03T00:00:00Z"
                }
            }
        }
    ]
    formatted_data = format_data(sample_data, "data_eco_datasets")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == 2
    for dataset in formatted_data:
        assert "id" in dataset
        assert "title" in dataset
        assert "publisher" in dataset
        assert "created_at" in dataset
        assert "updated_at" in dataset


def test_format_data_eco_discussions():
    sample_data = [
        {
            "id_jdd": "dataset_1",
            "id": "1",
            "id_parent": "0",
            "sujet": "Discussion 1",
            "pseudo": "User1",
            "commentaire": "First message",
            "horodotage": "2023-01-01T00:00:00Z",
            "username": "user1"
        },
        {
            "id_jdd": "dataset_2",
            "id": "2",
            "id_parent": "0",
            "sujet": "Discussion 2",
            "pseudo": "User2",
            "commentaire": "Second message",
            "horodotage": "2023-01-02T00:00:00Z",
            "username": "user2"
        }
    ]
    formatted_data = format_data(sample_data, "data_eco_discussions")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == 2
    for discussion in formatted_data:
        assert "id_jdd" in discussion
        assert "id_message" in discussion
        assert "id_parent_message" in discussion
        assert "title" in discussion
        assert "pseudo" in discussion
        assert "comment" in discussion
        assert "date" in discussion
        assert "username" in discussion


def test_save_to_csv():
    sample_data = [
        {"id": "1", "title": "Discussion 1", "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-02T00:00:00Z"},
        {"id": "2", "title": "Discussion 2", "created_at": "2023-01-03T00:00:00Z", "updated_at": "2023-01-04T00:00:00Z"}
    ]
    filename = "test_output.csv"
    save_to_csv(sample_data, filename)
    assert os.path.exists(filename)

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["id"] == "1"
        assert rows[1]["id"] == "2"

    os.remove(filename)  # Suppression du csv après le test