import abc
from typing import List
from domain.models import Message

class AbstractCommentRepository(abc.ABC):
    @abc.abstractmethod
    def get_message_by_sk(self, discussion_id: str) -> Message:
        pass

    @abc.abstractmethod
    def create_message(self, message: Message) -> None:
        pass

    @abc.abstractmethod
    def update_message(self, discussion_id: str, updated_message: dict) -> None:
        pass

    @abc.abstractmethod
    def delete_message(self, discussion_id: str) -> None:
        pass

    @abc.abstractmethod
    def get_all_messages(self) -> List[Message]:
        pass
