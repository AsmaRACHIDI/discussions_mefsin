from __future__ import annotations

class Message:
    def __init__(self, discussion_id: str, created: str, closed: bool, dataset_id: str, title: str, first_message: str, url_discussion: str, source: str, dataset_title: str, dataset_publisher: str, dataset_created_at: str, dataset_updated_at: str, dataset_url: str):
        self.discussion_id = discussion_id
        self.created = created
        self.closed = closed
        self.dataset_id = dataset_id
        self.title = title
        self.first_message = first_message
        self.url_discussion = url_discussion
        self.source = source
        self.dataset_title = dataset_title
        self.dataset_publisher = dataset_publisher
        self.dataset_created_at = dataset_created_at
        self.dataset_updated_at = dataset_updated_at
        self.dataset_url = dataset_url

    @classmethod
    def create(cls, discussion_id: str, created: str, closed: bool, dataset_id: str, title: str, first_message: str, url_discussion: str, source: str, dataset_title: str, dataset_publisher: str, dataset_created_at: str, dataset_updated_at: str, dataset_url: str) -> Message:
        return cls(discussion_id, created, closed, dataset_id, title, first_message, url_discussion, source, dataset_title, dataset_publisher, dataset_created_at, dataset_updated_at, dataset_url)
