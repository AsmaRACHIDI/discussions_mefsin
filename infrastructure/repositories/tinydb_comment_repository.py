from typing import List, Dict, Optional
from tinydb import TinyDB, Query, where
from domain.gateways import AbstractCommentRepository
from domain.models import Message
from core.config import Config

class TinyDBCommentRepository(AbstractCommentRepository):
    def __init__(self):
        self.db = TinyDB(Config.TINYDB_PATH)
        self.messages_table = self.db.table('messages')

    def get_message_by_sk(self, discussion_id: str) -> Optional[Message]:
        """Retrieve a message by discussion ID."""
        try:
            MessageQuery = Query()
            result = self.messages_table.get(MessageQuery.discussion_id == discussion_id)
            return Message(**result) if result else None
        except Exception as e:
            print(f"Error retrieving message: {e}")
            return None

    def add_message(self, message: Message) -> None:
        """Add a new message to the repository, avoiding duplicates."""
        try:
            existing_message = self.get_message_by_sk(message.discussion_id)
            if existing_message:
                print(f"Duplicate message found for discussion_id: {message.discussion_id}")
            else:
                self.messages_table.insert(message.__dict__)
        except Exception as e:
            print(f"Error adding message: {e}")

    def update_message(self, discussion_id: str, updated_message: Dict) -> None:
        """Update an existing message by discussion ID."""
        try:
            MessageQuery = Query()
            self.messages_table.update(updated_message, MessageQuery.discussion_id == discussion_id)
        except Exception as e:
            print(f"Error updating message: {e}")

    def delete_message(self, discussion_id: str) -> None:
        """Delete a message by discussion ID."""
        try:
            MessageQuery = Query()
            self.messages_table.remove(MessageQuery.discussion_id == discussion_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

    def get_all_messages(self) -> List[Message]:
        """Retrieve all messages from the repository."""
        try:
            return [Message(**item) for item in self.messages_table.all()]
        except Exception as e:
            print(f"Error retrieving all messages: {e}")
            return []

    def clear_db(self) -> None:
        """Clear all data from the messages table."""
        try:
            self.messages_table.truncate()
        except Exception as e:
            print(f"Error clearing the database: {e}")
