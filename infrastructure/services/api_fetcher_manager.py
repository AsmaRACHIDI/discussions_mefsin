# Gestion des Fetchers
from api.fetch_data import BaseFetcher, DataGouvFetcher, DataEcoFetcher
from core.config import Config

class APIFetcherManager:
    @staticmethod
    def get_client(api_type: str) -> BaseFetcher:
        if api_type == "data_gouv":
            return DataGouvFetcher(Config.DATA_GOUV_DISCUSSIONS_URL, Config.DATA_GOUV_DATASETS_URL)
        elif api_type == "data_eco":
            return DataEcoFetcher(Config.DATA_ECO_DISCUSSIONS_URL, Config.DATA_ECO_DATASETS_URL)
        else:
            raise ValueError(f"No client available for API type: {api_type}")

