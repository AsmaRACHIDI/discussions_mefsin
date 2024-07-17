from api.api_fetcher_manager import APIFetcherManager

class CommentService:
    def __init__(self, comment_data_access):
        self.comment_data_access = comment_data_access

    def fetch_and_store_discussions(self, api_type: str):
        fetcher = APIFetcherManager.get_fetcher(api_type)
        discussions = fetcher.fetch_discussions()
        if discussions:
            formatted_discussions = fetcher.format_data(discussions, f"{api_type}_discussions")
            self.comment_data_access.save_comments(formatted_discussions, f"{api_type}_discussions")

    def fetch_and_store_datasets(self, api_type: str):
        fetcher = APIFetcherManager.get_fetcher(api_type)
        datasets = fetcher.fetch_datasets()
        if datasets:
            formatted_datasets = fetcher.format_data(datasets, f"{api_type}_datasets")
            self.comment_data_access.save_comments(formatted_datasets, f"{api_type}_datasets")

    def get_all_comments(self, table_name):
        return self.comment_data_access.get_all_comments(table_name)

    def clear_data(self, table_name):
        self.comment_data_access.clear_table(table_name)

    def insert_comment(self, table_name, comment):
        self.comment_data_access.insert_comment(table_name, comment)

    def update_comment(self, table_name, comment_id, updated_fields):
        self.comment_data_access.update_comment(table_name, comment_id, updated_fields)

    def delete_comment(self, table_name, comment_id):
        self.comment_data_access.delete_comment(table_name, comment_id)
