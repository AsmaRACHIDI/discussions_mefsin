import json
import requests

from format import dump_json, append_to_csv

def fetch_data_from_data_gouv_api() -> dict:
#def fetch_data_from_data_gouv_api(api_url: str, page: int = 1) -> dict:
    """
    Récupère les discussions à partir de l'API de data.gouv.fr
    """
    api_url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lève une exception si la requête échoue
        data_json = response.json()
        # Sauvegarde les discussions formatées au format JSON
        dump_json("all_data_gouv_datasets.json", data_json)
        return data_json
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []


def fetch_data_from_data_eco_api() -> dict:
#def fetch_data_from_data_eco_api(api_url: str) -> dict:
    """
    Récupère les données brutes à partir de l'API de data.economie.gouv.fr
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
        response = requests.get(api_url, params=params)

        if response.status_code != 200:
            print(f"Error fetching data. Status code: {response.status_code}")
            return {}

        data = response.json()
        all_data.extend(data["results"])

        if len(data["results"]) < 100:  # Si le nombre d'éléments récupérés est inférieur à la limite par page, cela signifie que nous avons récupéré tous les éléments disponibles
            break

        params["offset"] += 100  # Déplacer l'offset pour récupérer la page suivante

        # Sauvegarde les discussions formatées au format JSON
        dump_json("all_data_eco_datasets.json", all_data)

    return all_data

def format_data(data_json, api_type):
    """
    Formate les données récupérées sous forme de liste
    """
    formatted_data = []

    if api_type == "data_gouv":
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
            ###
            ###
            ### CSV
            ###
            ###

    elif api_type == "data_eco":
        formatted_data = [{"id": dataset["dataset_id"], 
                           "uid": dataset["dataset_uid"], 
                           "title": dataset["metas"]["default"]["title"], 
                           "publisher": dataset["metas"]["default"]["publisher"], 
                           "url_source": dataset["metas"]["default"]["references"]
                           } for dataset in data_json]
        
    else:
        print("Type d'API non valide.")

    return formatted_data

def main(api_type):

    if api_type == "data_gouv":
        api_url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
   
    elif api_type == "data_eco":
        api_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"
    
    else:
        print("Type d'API non valide.")
        return
    
    # Récupère les données depuis l'API
    data_json = fetch_data_from_data_gouv_api() if api_type == "data_gouv" else fetch_data_from_data_eco_api()
    
    # Formate les données pour l'exportation CSV
    formatted_data = format_data(data_json, api_type)
    
    # Exporte les données au format CSV
    if api_type == "data_gouv":
        append_to_csv("data_gouv_datasets.csv", formatted_data)
    
    elif api_type == "data_eco":
        append_to_csv("data_eco_datasets.csv", formatted_data)
    
    else:
        print("Type d'API non valide.")

if __name__ == "__main__":
    main("data_gouv")
