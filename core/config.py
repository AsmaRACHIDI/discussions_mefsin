import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    TINYDB_PATH = os.getenv('TINYDB_PATH', 'db.json')
    API_KEY = os.getenv('API_KEY')
    DATA_GOUV_DISCUSSIONS_URL = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
    DATA_GOUV_DATASETS_URL = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/datasets"
    DATA_ECO_DISCUSSIONS_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/interne-discussions/records"
    DATA_ECO_DATASETS_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"
