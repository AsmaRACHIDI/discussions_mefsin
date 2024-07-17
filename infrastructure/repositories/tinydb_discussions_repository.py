from tinydb import TinyDB, Query
from domain.gateways import AbstractCommentRepository
from domain.models import Message
from core.config import Config


class TinyDBCommentRepository(AbstractCommentRepository):
    def __init__(self):
        self.db = TinyDB(Config.TINYDB_PATH)
        self.messages_table = self.db.table('messages')

    def get_message_by_sk(self, discussion_id: str) -> Message:
        result = self.messages_table.get(Query().discussion_id == discussion_id)
        return Message(**result) if result else None

    def create_message(self, message: Message) -> None:
        self.messages_table.insert(message.__dict__)
