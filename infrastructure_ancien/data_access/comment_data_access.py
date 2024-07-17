from tinydb import Query

# Opérations CRUD
# Méthodes pour manipuler les données stockées dans la base TinyDB
class CommentDataAccess:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def save_comments(self, comments, table_name):
        for comment in comments:
            self.db_connector.insert(table_name, comment)

    def get_all_comments(self, table_name):
        return self.db_connector.all(table_name)

    def find_comment_by_id(self, comment_id, table_name):
        Comment = Query()
        return self.db_connector.search(table_name, Comment.id == comment_id)

    def clear_table(self, table_name):
        self.db_connector.clear(table_name)

    def insert_comment(self, table_name, comment):
        self.db_connector.insert(table_name, comment)

    def update_comment(self, table_name, comment_id, updated_fields):
        Comment = Query()
        self.db_connector.update(table_name, updated_fields, Comment.id == comment_id)

    def delete_comment(self, table_name, comment_id):
        Comment = Query()
        self.db_connector.remove(table_name, Comment.id == comment_id)
