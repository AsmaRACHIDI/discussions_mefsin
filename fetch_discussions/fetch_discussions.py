import json
import requests
from format import dump_json, open_json, append_to_csv

def fetch_discussions(api_url):
    """
    Récupère les discussions à partir de l'API de data.gouv.fr
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lève une exception si la requête échoue
        data_json = response.json()
        # Sauvegarde les discussions formatées au format JSON
        dump_json("app/static/data/dataset.json", data_json)
        return data_json
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

def format_discussions(data_json):
    """
    Formate les discussions sous forme de liste
    """
    formatted_discussions = []
    for discussion in data_json:
        formatted_discussion = {
            "id": discussion["id"],
            "created": discussion["created"],
            "dataset_id": discussion["subject"]["id"],
            "title": discussion["title"],
            "first_message": discussion["discussion"][0]["content"]
        }
        # for message in discussion["formatted_discussion"]:
    #     out = {
    #         **formatted_discussion,
    #         "message": message["content"]
    #     }
        formatted_discussions.append(formatted_discussion)
    return formatted_discussions

def main():
    # toutes les discussions de data.gouv.fr
    api_url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
    # 1 discussion de rappel conso
    #api_url = "https://www.data.gouv.fr/api/1/datasets/rappelconso/#/discussions"
    
    # Récupère les discussions depuis l'API
    data_json = fetch_discussions(api_url)
    
    # Formate les discussions pour l'exportation CSV
    formatted_discussions = format_discussions(data_json)
    
    # Ajoute les discussions formatées à un fichier CSV
    append_to_csv("static/data/dataset.csv", formatted_discussions)

if __name__ == "__main__":
    main()
