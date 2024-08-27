from __future__ import annotations

class Message:
    def __init__(self, discussion_id: str, discussion_created: str, discussion_closed: bool, dataset_id: str, parent_discussion_id: str, discussion_title: str, comment: str, url_discussion: str, dataset_title: str, dataset_publisher: str, dataset_created_at: str, dataset_updated_at: str, dataset_url: str, source: str = None):
        self.discussion_id = discussion_id
        self.discussion_created = discussion_created
        self.discussion_closed = discussion_closed
        self.dataset_id = dataset_id
        self.parent_discussion_id = parent_discussion_id
        self.discussion_title = discussion_title
        self.comment = comment
        self.url_discussion = url_discussion
        self.dataset_title = dataset_title
        self.dataset_publisher = dataset_publisher
        self.dataset_created_at = dataset_created_at
        self.dataset_updated_at = dataset_updated_at
        self.dataset_url = dataset_url
        self.source = source

    @classmethod
    def create(cls, discussion_id: str, discussion_created: str, discussion_closed: bool, dataset_id: str, parent_discussion_id: str, discussion_title: str, comment: str, url_discussion: str, dataset_title: str, dataset_publisher: str, dataset_created_at: str, dataset_updated_at: str, dataset_url: str, source: str = None) -> Message:
        return cls(discussion_id, discussion_created, discussion_closed, dataset_id, parent_discussion_id, discussion_title, comment, url_discussion, dataset_title, dataset_publisher, dataset_created_at, dataset_updated_at, dataset_url, source)

    def to_dict(self) -> dict:
        return {
            'discussion_id': self.discussion_id,
            'discussion_created': self.discussion_created,
            'discussion_closed': self.discussion_closed,
            'dataset_id': self.dataset_id,
            'parent_discussion_id': self.parent_discussion_id,
            'discussion_title': self.discussion_title,
            'comment': self.comment,
            'url_discussion': self.url_discussion,
            'dataset_title': self.dataset_title,
            'dataset_publisher': self.dataset_publisher,
            'dataset_created_at': self.dataset_created_at,
            'dataset_updated_at': self.dataset_updated_at,
            'dataset_url': self.dataset_url,
            'source': self.source
        }
