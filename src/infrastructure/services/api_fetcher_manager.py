# Gestion des Fetchers
from src.domain.gateways import BaseFetcher
from src.infrastructure.services.fetch_data import DataGouvFetcher, DataEcoFetcher
from src.core.config import Config


class APIFetcherManager:
    @staticmethod
    def get_client(api_type: str) -> BaseFetcher:
        if api_type == "data_gouv":
            return DataGouvFetcher(Config.DATA_GOUV_DISCUSSIONS_URL, Config.DATA_GOUV_DATASETS_URL)
        elif api_type == "data_eco":
            return DataEcoFetcher(Config.DATA_ECO_DISCUSSIONS_URL, Config.DATA_ECO_DATASETS_URL)
        else:
            raise ValueError(f"No client available for API type: {api_type}")
