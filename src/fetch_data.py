import json
import requests
import os
import csv
import logging
import click
from typing import List, Dict, Optional
from dotenv import load_dotenv
from src.format import dump_json

load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API key
HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}

def fetch_discussions_from_data_gouv_api() -> Optional[List[Dict]]:
    """
    Fetches discussions from the data.gouv.fr API

    Returns:
        Optional[List[Dict]]: List of discussions or None in case of an error.
    """
    api_url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data_json = response.json()
        logging.info("Discussions from data.gouv.fr fetched successfully!")
        dump_json("app/static/data/all_data_gouv_discussions.json", data_json)
        return data_json
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return None

def fetch_datasets_from_data_gouv_api() -> Optional[List[Dict]]:
    """
    Fetches datasets information from the data.gouv.fr API

    Returns:
        Optional[List[Dict]]: List of datasets or None in case of an error.
    """
    base_url = "https://www.data.gouv.fr/api/1/organizations"
    organization = "ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique"
    resource = "datasets"

    datasets = []
    page = 1

    while True:
        url = f"{base_url}/{organization}/{resource}?page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            logging.error(f"Error fetching data for page {page}. Status code: {response.status_code}")
            break

        data = response.json()

        if not data["data"]:
            break

        datasets.extend(data["data"])

        page += 1

    # Save JSON data to a file
    with open("app/static/data/all_data_gouv_datasets.json", "w") as json_file:
        json.dump(datasets, json_file, indent=2)
    logging.info("Data has been saved to 'all_data_gouv_datasets.json'")

    return datasets 

def fetch_discussions_from_data_eco_api() -> Optional[Dict[str, List[Dict]]]:
    """
    Fetches discussions from the data.economie.gouv.fr API

    Returns:
        Optional[Dict[str, List[Dict]]]: Dictionary containing discussions and the total number of discussions or None in case of an error.
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

def fetch_datasets_from_data_eco_api() -> Optional[List[Dict]]:
    """
    Fetches datasets information from the data.economie.gouv.fr API

    Returns:
        Optional[List[Dict]]: List of datasets or None in case of an error.
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

def format_data(data_json: List[Dict], api_type: str) -> List[Dict]:
    """
    Formats the fetched data into a list.

    Args:
        data_json (List[Dict]): JSON data to format.
        api_type (str): Type of API for formatting.

    Returns:
        List[Dict]: Formatted data.
    """
    formatted_data = []

    if api_type == "data_gouv_discussions":
        for discussion in data_json:
            formatted_discussion = {
                "discussion_id": discussion["id"],
                "created": discussion["created"],
                "closed": discussion["closed"],
                "dataset_id": discussion["subject"]["id"],
                "title": discussion["title"],
                "first_message": discussion["discussion"][0]["content"],
                "url_discussion": discussion["url"],
                "source": "data_gouv"
            }
            formatted_data.append(formatted_discussion)

    elif api_type == "data_gouv_datasets":
        formatted_data = [
            {
                "dataset_id": dataset["id"],
                "slug": dataset["slug"],
                "title": dataset["title"],
                "url": dataset["page"],
                "source": "data_gouv"
            } for dataset in data_json
        ]

    elif api_type == "data_eco_discussions":
        formatted_data = [
            {
                "jdd_id": discussion["id_jdd"],
                "message_id": discussion["id"],
                "parent_message_id": discussion["id_parent"],
                "title": discussion["sujet"],
                "pseudo": discussion["pseudo"],
                "comment": discussion["commentaire"],
                "date": discussion["horodatage"],
                "username": discussion["username"],
                "source": "data_eco"
            } for discussion in data_json
        ]

    elif api_type == "data_eco_datasets":
        formatted_data = [
            {
                "dataset_id": dataset["dataset_id"],
                "title": dataset["metas"]["default"]["title"],
                "publisher": dataset["metas"]["default"]["publisher"],
                "created_at": dataset["metas"]["dcat"]["created"],
                "updated_at": dataset["metas"]["default"]["modified"],
                "source": "data_eco"
            } for dataset in data_json
        ]

    else:
        logging.warning("Invalid API type.")
        return []

    logging.info(f"Data formatted for API type: {api_type}")
    return formatted_data

def save_to_csv(data: List[Dict], filename: str):
    """
    Saves the data to a CSV file.

    Args:
        data (List[Dict]): Data to save.
        filename (str): CSV file name.
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

# def aggregate_datasets(data_gouv: List[Dict], data_eco: List[Dict]) -> List[Dict]:
#     """
#     Aggregates datasets and discussions from different sources.

#     Args:
#         data_gouv_discussions (List[Dict]): Discussions data from data.gouv.fr
#         data_gouv_datasets (List[Dict]): Datasets data from data.gouv.fr
#         data_eco_datasets (List[Dict]): Datasets data from data.economie.gouv.fr
#         data_eco_discussions (List[Dict]): Discussions data from data.economie.gouv.fr

#     Returns:
#         List[Dict]: Aggregated data.
#     """
#     aggregated_data = data_gouv + data_eco
#     logging.info("Datasets from data_gouv and data_eco aggregated successfully.")
#     return aggregated_data

@click.command()
@click.argument('api_type', type=click.Choice(['data_gouv', 'data_eco']), nargs=-1, required=False)
def main(api_type: List[str]):
    """
    Main entry point of the script.

    Args:
        api_type (List[str]): Type of API to query (data_gouv, data_eco, or both).
    """
    if not api_type:  # If no argument is specified, run both API types
        api_type = ["data_gouv", "data_eco"]

    # data_gouv_discussions = []
    # data_gouv_datasets = []
    # data_eco_discussions = []
    # data_eco_datasets = []
    
    for api in api_type:
        logging.info(f"Fetching data from {api} API:")
        if api == "data_gouv":
            data_json = fetch_discussions_from_data_gouv_api()
            if data_json:
                formatted_data = format_data(data_json, "data_gouv_discussions")
                save_to_csv(formatted_data, "app/static/data/data_gouv_discussions.csv")
                #data_gouv_discussions = formatted_data

            # Call the function to fetch datasets
            datasets_json = fetch_datasets_from_data_gouv_api()
            if datasets_json:
                formatted_datasets = format_data(datasets_json, "data_gouv_datasets")
                save_to_csv(formatted_datasets, "app/static/data/data_gouv_datasets.csv")
                #data_gouv_datasets = formatted_datasets
       
        elif api == "data_eco":
            data_json_discussions = fetch_discussions_from_data_eco_api()
            if data_json_discussions:
                formatted_data_discussions = format_data(data_json_discussions["records"], "data_eco_discussions")
                save_to_csv(formatted_data_discussions, "app/static/data/data_eco_discussions.csv")
                #data_eco_discussions = formatted_data_discussions

            data_json_datasets = fetch_datasets_from_data_eco_api()
            if data_json_datasets:
                formatted_data_datasets = format_data(data_json_datasets, "data_eco_datasets")
                save_to_csv(formatted_data_datasets, "app/static/data/data_eco_datasets.csv")
                #data_eco_datasets = formatted_data_datasets
        
        else:
            logging.warning("Invalid API type.")

        # Aggregation of datasets and discussions
        #aggregated_datasets = aggregate_datasets(data_gouv_discussions, data_gouv_datasets, data_eco_datasets, data_eco_discussions)
        #save_to_csv(aggregated_datasets, "app/static/data/aggregated_datasets.csv")

if __name__ == "__main__":
    main()
