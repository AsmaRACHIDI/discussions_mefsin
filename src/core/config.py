import os
from dotenv import load_dotenv

load_dotenv()

os.makedirs("data/raw", exist_ok=True)
# os.makedirs("trained_models/", exist_ok=True)

class Config:
    # Chargement des variables d'environnement
    TINYDB_PATH = os.getenv("TINYDB_PATH", "data/raw/tinydb.json")

    API_KEY = os.getenv("API_KEY")
    
    organization_name = os.getenv("ORGANIZATION_NAME")

    #DATA_GOUV_DISCUSSIONS_URL = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
    #DATA_GOUV_DATASETS_URL = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/datasets"
    
    DATA_GOUV_DISCUSSIONS_URL = f"https://www.data.gouv.fr/api/1/organizations/{organization_name}/discussions"
    DATA_GOUV_DATASETS_URL = f"https://www.data.gouv.fr/api/1/organizations/{organization_name}/datasets"


    DATA_ECO_DISCUSSIONS_URL = (
        "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/interne-discussions/records"
    )
    DATA_ECO_DATASETS_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"

    MODEL1_ZIP_FILE = os.getenv("MODEL1_ZIP_FILE", "trained_models/bert-finetuned-my-data-final_archive.zip")
    MODEL2_ZIP_FILE = os.getenv("MODEL2_ZIP_FILE", "trained_models/bert-finetuned-my-data-final2_archive2.zip")
