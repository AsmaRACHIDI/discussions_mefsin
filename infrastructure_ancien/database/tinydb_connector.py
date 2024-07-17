from tinydb import TinyDB, Query
from core.config import Config

# Classe pour interagir avec la base TinyDB
class TinyDBConnector:
    def __init__(self):
        self.db = TinyDB(Config.TINYDB_PATH)

    def insert(self, table_name, data):
        table = self.db.table(table_name)
        table.insert(data)

    def insert_multiple(self, table_name, data_list):
        table = self.db.table(table_name)
        table.insert_multiple(data_list)

    def search(self, table_name, query):
        table = self.db.table(table_name)
        return table.search(query)

    def all(self, table_name):
        table = self.db.table(table_name)
        return table.all()

    def clear(self, table_name):
        table = self.db.table(table_name)
        table.truncate()