import pytest
import os
from dotenv import load_dotenv

from tmp import fetch_discussions_from_data_gouv_api, fetch_datasets_from_data_eco_api, fetch_discussions_from_data_eco_api, format_data

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


def test_format_data_data_gouv():
    data_json = [
        {"id": 1, "created": "2024-05-15", "closed": True, "subject": {"id": 123}, "title": "Discussion 1", "discussion": [{"content": "Message 1"}]},
        {"id": 2, "created": "2024-05-16", "closed": False, "subject": {"id": 456}, "title": "Discussion 2", "discussion": [{"content": "Message 2"}]}
    ]
    formatted_data = format_data(data_json, "data_gouv")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == 2
    assert "id" in formatted_data[0]
    assert "created" in formatted_data[0]

def test_format_data_data_eco_gouv():
    data_json = [
        {"id": 1, "name": "Dataset 1"},
        {"id": 2, "name": "Dataset 2"}
    ]
    formatted_data = format_data(data_json, "data_eco_gouv")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == 2
    assert "id" in formatted_data[0]
    assert "name" in formatted_data[0]
