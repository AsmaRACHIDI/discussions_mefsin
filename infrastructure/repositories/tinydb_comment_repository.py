from typing import List, Dict
from tinydb import TinyDB, Query
from domain.gateways import AbstractCommentRepository
from domain.models import Message
from core.config import Config

class TinyDBCommentRepository(AbstractCommentRepository):
    def __init__(self):
        self.db = TinyDB(Config.TINYDB_PATH) # db = TinyDB('db.json')
        self.messages_table = self.db.table('messages')

    def get_message_by_sk(self, discussion_id: str) -> Message:
        MessageQuery = Query()
        result = self.messages_table.get(MessageQuery.discussion_id == discussion_id)
        return Message(**result) if result else None

    def add_message(self, message: Message) -> None:
        if not self.get_message_by_sk(message.discussion_id):
            self.messages_table.insert(message.__dict__)
        else:
            print(f"Duplicate message found for discussion_id: {message.discussion_id}")

    def update_message(self, discussion_id: str, updated_message: Dict) -> None:
        MessageQuery = Query()
        self.messages_table.update(updated_message, MessageQuery.discussion_id == discussion_id)

    def delete_message(self, discussion_id: str) -> None:
        MessageQuery = Query()
        self.messages_table.remove(MessageQuery.discussion_id == discussion_id)

    def get_all_messages(self) -> List[Message]:
        return [Message(**item) for item in self.messages_table.all()]

    def clear_db(self) -> None:
        self.messages_table.truncate()
