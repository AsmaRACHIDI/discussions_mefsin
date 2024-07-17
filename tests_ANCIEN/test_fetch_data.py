import pytest
import os
import csv
import json

from dotenv import load_dotenv
from src.fetch_data import fetch_discussions_from_data_gouv_api, fetch_datasets_from_data_gouv_api, fetch_datasets_from_data_eco_api, fetch_discussions_from_data_eco_api, format_data, save_to_csv

# Récupération des variables d'environnement
load_dotenv()


def load_sample_data(filepath, fixture_name):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # Pour discussions_data_eco
    # Vérifiez si 'records' est une clé dans le dictionnaire des données
    if 'records' in data:
        sample_data = data['records'][:2]  # Récupère les deux premiers éléments de la liste 'records'
    else:
        sample_data = data[:2]

    fixture_path = os.path.join('fixtures', f'{fixture_name}.json')
    with open(fixture_path, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=4, ensure_ascii=False)

    return sample_data


def test_fetch_discussions_from_data_gouv_api():
    data = fetch_discussions_from_data_gouv_api()
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)  # Vérifie que le premier élément de la liste est un dictionnaire


def test_fetch_datasets_from_data_gouv_api():
    data = fetch_datasets_from_data_gouv_api()
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict) 


def test_fetch_discussions_from_data_eco_api():
    data = fetch_discussions_from_data_eco_api()
    assert isinstance(data, dict)
    assert "records" in data
    assert "total_count" in data
    assert len(data["records"]) > 0
    assert len(data["records"]) == data["total_count"]
    assert isinstance(data["records"][0], dict)
    print(len(data["records"]))


def test_fetch_datasets_from_data_eco_api():
    data = fetch_datasets_from_data_eco_api()
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict) 


def test_format_data_gouv_discussions():
    sample_data = load_sample_data('app/static/data/all_data_gouv_discussions.json', 'data_gouv_discussions_sample')
    formatted_data = format_data(sample_data, "data_gouv_discussions")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == len(sample_data)
    for discussion in formatted_data:
        assert "id" in discussion
        assert "created" in discussion
        assert "closed" in discussion
        assert "dataset_id" in discussion
        assert "title" in discussion
        assert "first_message" in discussion
        assert "url_discussion" in discussion


def test_format_data_gouv_datasets():
    sample_data = load_sample_data('app/static/data/all_data_gouv_datasets.json', 'data_gouv_datasets_sample')
    formatted_data = format_data(sample_data, "data_gouv_datasets")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == len(sample_data)
    for dataset in formatted_data:
        assert "dataset_id" in dataset
        assert "slug" in dataset
        assert "title" in dataset
        assert "url" in dataset


def test_format_data_eco_discussions():
    sample_data = load_sample_data('app/static/data/all_data_eco_discussions.json', 'data_eco_discussions_sample')
    formatted_data = format_data(sample_data, "data_eco_discussions")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == len(sample_data)
    for discussion in formatted_data:
        assert "jdd_id" in discussion
        assert "message_id" in discussion
        assert "parent_message_id" in discussion
        assert "title" in discussion
        assert "pseudo" in discussion
        assert "comment" in discussion
        assert "date" in discussion
        assert "username" in discussion


def test_format_data_eco_datasets():
    sample_data = load_sample_data('app/static/data/all_data_eco_datasets.json', 'data_eco_datasets_sample')
    formatted_data = format_data(sample_data, "data_eco_datasets")
    assert isinstance(formatted_data, list)
    assert len(formatted_data) == len(sample_data)
    for dataset in formatted_data:
        assert "id" in dataset
        assert "title" in dataset
        assert "publisher" in dataset
        assert "created_at" in dataset
        assert "updated_at" in dataset



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