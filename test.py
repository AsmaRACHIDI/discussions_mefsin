import os
import requests
from dotenv import load_dotenv
from format import dump_json, open_json, append_to_csv

load_dotenv()

api_url = "https://data.economie.gouv.fr/api/automation/v1.0/datasets/"

# Clé d'API
HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}

def get_datasets(api_url, headers):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Will raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def get_feedbacks(dataset_uid, headers):
    feedbacks_url = f"{api_url}{dataset_uid}/feedbacks/"
    try:
        response = requests.get(feedbacks_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error for dataset {dataset_uid}: {http_err}")
    except Exception as err:
        print(f"Other error for dataset {dataset_uid}: {err}")
    return None

def main():
    datasets = get_datasets(api_url, HEADERS)
    if datasets:
        dump_json("discussions_data_eco.json", datasets)

        for dataset in datasets['results']:
            dataset_uid = dataset['uid']
            feedbacks = get_feedbacks(dataset_uid, HEADERS)
            if feedbacks:
                print(f"Feedbacks pour le dataset {dataset_uid}: {feedbacks}")
                # Append feedbacks to a CSV file (example function, implement as needed)
                append_to_csv("feedbacks.csv", feedbacks)
            else:
                print(f"Impossible de récupérer les feedbacks pour le dataset {dataset_uid}")
    else:
        print("La requête pour récupérer les datasets a échoué.")

if __name__ == "__main__":
    main()
