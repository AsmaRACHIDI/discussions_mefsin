import json
import requests
import os
import csv
import logging
import click

from dotenv import load_dotenv
from format import dump_json
from typing import List, Dict, Union, Optional

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clé d'API
HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}


def fetch_discussions_from_data_gouv_api() -> Optional[List[Dict]]:
    """
    Récupère les discussions à partir de l'API de data.gouv.fr

    Returns:
        List[Dict]: Liste de discussions ou None en cas d'erreur.
    """
    api_url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data_json = response.json()
        logging.info("Discussions from data.gouv.fr fetched successfully.")
        dump_json("app/static/data/all_data_gouv_discussions.json", data_json)
        return data_json
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la requête : {e}")
        return None


def fetch_datasets_from_data_eco_api() -> List[Dict]:
    """
    Récupère les datasets à partir de l'API de data.economie.gouv.fr

    Returns:
        List[Dict]: Liste de datasets.
    """
    all_data = []
    api_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"
    params = {
        "timezone": "UTC",
        "include_links": "false",
        "include_app_metas": "false",
        "limit": 100,
        "offset": 0
    }

    while True:
        try:
            response = requests.get(api_url, headers=HEADERS, params=params)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data["results"])

            if len(data["results"]) < 100:
                break

            params["offset"] += 100
        except requests.RequestException as e:
            logging.error(f"Error fetching datasets: {e}")
            break

    dump_json("app/static/data/all_data_eco_datasets.json", all_data)
    logging.info("Datasets from data.economie.gouv.fr fetched successfully.")
    return all_data


def fetch_discussions_from_data_eco_api() -> Optional[Dict[str, Union[List[Dict], int]]]:
    """
    Récupère les données brutes à partir de l'API de data.economie.gouv.fr

    Returns:
        Dict[str, Union[List[Dict], int]]: Dictionnaire contenant les discussions et le nombre total de discussions ou None en cas d'erreur.
    """
    api_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/interne-discussions/records"
    all_data = []
    limit = 100
    offset = 0
    total_count = 0

    try:
        while True:
            response = requests.get(api_url, headers=HEADERS, params={"limit": limit, "offset": offset})
            response.raise_for_status()
            data_json = response.json()
            total_count = data_json["total_count"]
            records = data_json.get('results', [])

            if not records:
                break

            all_data.extend(records)
            offset += limit

        dump_json("app/static/data/all_data_eco_discussions.json", {"records": all_data})
        logging.info("Discussions from data.economie.gouv.fr fetched successfully.")
        return {"records": all_data, "total_count": total_count}
    except requests.RequestException as e:
        logging.error(f"HTTP error occurred: {e}")
    except Exception as e:
        logging.error(f"Other error occurred: {e}")
    return None


def format_data(data_json: List[Dict], api_type: str) -> List[Dict]:
    """
    Formate les données récupérées sous forme de liste.

    Args:
        data_json (List[Dict]): Données JSON à formater.
        api_type (str): Type de l'API pour le formatage.

    Returns:
        List[Dict]: Données formatées.
    """
    formatted_data = []

    if api_type == "data_gouv_discussions":
        for discussion in data_json:
            formatted_discussion = {
                "id": discussion["id"],
                "created": discussion["created"],
                "closed": discussion["closed"],
                "dataset_id": discussion["subject"]["id"],
                "title": discussion["title"],
                "first_message": discussion["discussion"][0]["content"],
                "url_discussion": discussion["url"]
            }
            formatted_data.append(formatted_discussion)

    elif api_type == "data_eco_datasets":
        formatted_data = [
            {
                "id": dataset["dataset_id"],
                "title": dataset["metas"]["default"]["title"],
                "publisher": dataset["metas"]["default"]["publisher"],
                "created_at": dataset["metas"]["dcat"]["created"],
                "updated_at": dataset["metas"]["default"]["modified"]
            } for dataset in data_json
        ]

    elif api_type == "data_eco_discussions":
        formatted_data = [
            {
                "id_jdd": discussion["id_jdd"],
                "id_message": discussion["id"],
                "id_parent_message": discussion["id_parent"],
                "title": discussion["sujet"],
                "pseudo": discussion["pseudo"],
                "comment": discussion["commentaire"],
                "date": discussion["horodatage"],
                "username": discussion["username"]
            } for discussion in data_json
        ]

    else:
        logging.warning("Type d'API non valide.")
        return []

    logging.info(f"Data formatted for API type: {api_type}")
    return formatted_data


def save_to_csv(data: List[Dict], filename: str):
    """
    Sauvegarde les données au format CSV.

    Args:
        data (List[Dict]): Données à sauvegarder.
        filename (str): Nom du fichier CSV.
    """
    if not data:
        logging.warning("No data to save")
        return

    keys = data[0].keys()

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        logging.info(f"The data was saved in the file {filename}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")



@click.command()
@click.argument('api_type', type=click.Choice(['data_gouv', 'data_eco']), nargs=-1, required=False)
def main(api_type: List[str]):
    """
    Point d'entrée principal du script.

    Args:
        api_type (List[str]): Type d'API à interroger (data_gouv, data_eco ou les deux).
    """
    if not api_type:  # Si aucun argument n'est spécifié, exécutez les deux types d'API
        api_type = ["data_gouv", "data_eco"]

    for api in api_type:
        logging.info(f"Fetchning data from {api_type} API :")
        if api == "data_gouv":
            data_json = fetch_discussions_from_data_gouv_api()
            if data_json:
                formatted_data = format_data(data_json, "data_gouv_discussions")
                save_to_csv(formatted_data, "app/static/data/data_gouv_discussions.csv")
       
        elif api == "data_eco":
            data_json_datasets = fetch_datasets_from_data_eco_api()
            if data_json_datasets:
                formatted_data_datasets = format_data(data_json_datasets, "data_eco_datasets")
                save_to_csv(formatted_data_datasets, "app/static/data/data_eco_datasets.csv")

            data_json_discussions = fetch_discussions_from_data_eco_api()
            if data_json_discussions:
                formatted_data_discussions = format_data(data_json_discussions["records"], "data_eco_discussions")
                save_to_csv(formatted_data_discussions, "app/static/data/data_eco_discussions.csv")
        
        else:
            logging.warning("Type d'API non valide.")


if __name__ == "__main__":
    main()
