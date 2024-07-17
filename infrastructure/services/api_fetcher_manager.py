# infrastructure/services/api_fetcher_manager.py
from api.fetch_data import BaseFetcher, DataGouvFetcher, DataEcoFetcher

class APIFetcherManager:
    @staticmethod
    def get_client(api_type: str) -> BaseFetcher:
        if api_type == "data_gouv":
            discussions_url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/discussions"
            datasets_url = "https://www.data.gouv.fr/api/1/organizations/ministere-de-leconomie-des-finances-et-de-la-souverainete-industrielle-et-numerique/datasets"
            return DataGouvFetcher(discussions_url, datasets_url)
        
        elif api_type == "data_eco":
            discussions_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/interne-discussions/records"
            datasets_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"
            return DataEcoFetcher(discussions_url, datasets_url)
        
        else:
            raise ValueError(f"No client available for API type: {api_type}")
