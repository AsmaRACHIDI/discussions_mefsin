import abc
from domain.models import Message


class AbstractCommentRepository(abc.ABC):
    @abc.abstractmethod
    def get_message_by_sk(self, discussion_id: str) -> Message:
        pass  # pragma: no cover

    @abc.abstractmethod
    def create_message(self, message: Message) -> None:
        pass  # pragma: no cover
