import logging
from infrastructure.repositories.tinydb_comment_repository import TinyDBCommentRepository
from domain.usecases import FetchAndStoreDiscussions
from core.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_data():
    repository = TinyDBCommentRepository()

    logging.info("Fetching and storing discussions from data_gouv...")
    fetch_and_store_data_gouv = FetchAndStoreDiscussions(repository, "data_gouv")
    fetch_and_store_data_gouv.execute()
    logging.info("Data from data_gouv fetched and stored successfully.")

    logging.info("Fetching and storing discussions from data_eco...")
    fetch_and_store_data_eco = FetchAndStoreDiscussions(repository, "data_eco")
    fetch_and_store_data_eco.execute()
    logging.info("Data from data_eco fetched and stored successfully.")

if __name__ == "__main__":
    update_data()