import json
import requests
import os
import csv

from dotenv import load_dotenv
from format import dump_json, append_to_csv

load_dotenv()

# Clé d'API
HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}


def fetch_discussions_from_data_gouv_api() -> list:
    """
    Récupère les discussions à partir de l'API de data.gouv.fr
    """
    api_url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data_json = response.json()
        print(data_json)
        # Sauvegarde les discussions formatées au format JSON
        dump_json("app/static/data/all_data_gouv_discussions.json", data_json)
        return data_json
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []


def fetch_datasets_from_data_eco_api() -> list:
    """
    Récupère les datasets à partir de l'API de data.economie.gouv.fr
    """
    all_data = []

    api_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"

    params = {
        "timezone": "UTC",
        "include_links": "false",
        "include_app_metas": "false",
        "limit": 100,  # Modifier le nombre d'éléments par page selon vos besoins
        "offset": 0  # Commencer à partir du premier élément
    }

    while True:
        response = requests.get(api_url, headers=HEADERS, params=params)
        #response.raise_for_status()

        if response.status_code != 200:
            print(f"Error fetching data. Status code: {response.status_code}")
            return {}

        # Récupération et ajout des résultats
        data = response.json()
        all_data.extend(data["results"])

        # Condition de sortie
        if len(data["results"]) < 100:  # Si le nombre d'éléments récupérés est inférieur à la limite par page, cela signifie que nous avons récupéré tous les éléments disponibles
            break

        params["offset"] += 100  # Déplacer l'offset pour récupérer la page suivante

    # Sauvegarde les discussions formatées au format JSON
    dump_json("app/static/data/all_data_eco_datasets.json", all_data)

    return all_data


def fetch_discussions_from_data_eco_api() -> list:
    """
    Récupère les données brutes à partir de l'API de data.economie.gouv.fr
    """
    api_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/interne-discussions/records"

    all_data = []
    limit = 100  # Le nombre de résultats par page (ajustez selon la documentation de l'API)
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
        
        # Sauvegarde les discussions formatées au format JSON
        dump_json("app/static/data/all_data_eco_discussions.json", {"records": all_data})
        return {"records": all_data, "total_count": total_count}

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None


def format_data(data_json, api_type):
    """
    Formate les données récupérées sous forme de liste
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
            formatted_data = [{"id": dataset["dataset_id"], 
                            "title": dataset["metas"]["default"]["title"], 
                            "publisher": dataset["metas"]["default"]["publisher"],
                            "created_at": dataset["metas"]["dcat"]["created"], 
                            "updated_at": dataset["metas"]["default"]["modified"]
                            } for dataset in data_json]

    elif api_type == "data_eco_discussions":
        formatted_data = [{"id_jdd": discussion["id_jdd"], 
                           "id_message": discussion["id"], 
                           "id_parent_message": discussion["id_parent"], 
                           "title": discussion["sujet"], 
                           "pseudo": discussion["pseudo"], 
                           "comment": discussion["commentaire"],
                           "date": discussion["horodotage"],
                           "username": discussion["username"]
                           } for discussion in data_json]
        
    else:
        print("Type d'API non valide.")

    return formatted_data


def save_to_csv(data: list, filename: str):
    """
    Sauvegarde les données au format CSV.
    """
    if not data:
        print("Aucune donnée à sauvegarder")
        return

    keys = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

    print(f"Les données ont été sauvegardées dans le fichier {filename}")

def main(api_type):

    if api_type == "data_gouv":
        data_json = fetch_discussions_from_data_gouv_api()
        formatted_data = format_data(data_json, "data_gouv_discussions")
        save_to_csv(formatted_data, "app/static/data/data_gouv_discussions.csv")
   
    elif api_type == "data_eco":
        data_json_datasets = fetch_datasets_from_data_eco_api()
        formatted_data_datasets = format_data(data_json_datasets, "data_eco_datasets")
        save_to_csv(formatted_data_datasets, "app/static/data/data_eco_datasets.csv")

        data_json_discussions = fetch_discussions_from_data_eco_api()
        formatted_data_discussions = format_data(data_json_discussions, "data_eco_discussions")
        save_to_csv(formatted_data_discussions, "app/static/data/data_eco_discussions.csv")
    
    else:
        print("Type d'API non valide.")

if __name__ == "__main__":
    main("data_gouv")
    main("data_eco")