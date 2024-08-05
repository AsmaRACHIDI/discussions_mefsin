# update_data.py
from infrastructure.repositories.tinydb_comment_repository import TinyDBCommentRepository
from domain.usecases import FetchAndStoreDiscussions

repository = TinyDBCommentRepository()

fetch_and_store_data_gouv_discussions = FetchAndStoreDiscussions(repository, "data_gouv")
fetch_and_store_data_eco_discussions = FetchAndStoreDiscussions(repository, "data_eco")

def update_data():
    fetch_and_store_data_gouv_discussions.execute()
    fetch_and_store_data_eco_discussions.execute()

if __name__ == "__main__":
    update_data()
