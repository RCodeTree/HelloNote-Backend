"""面板业务逻辑层：聚合统计、最近笔记与标签。"""
from sqlalchemy.orm import Session

from app.models.note import Note
from app.models.tag import Tag
from app.repositories.note_repository import NoteRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.dashboard import DashboardStats


class DashboardService:
    def __init__(self, db: Session, user_id: int) -> None:
        self.user_id = user_id
        self.note_repo = NoteRepository(db)
        self.tag_repo = TagRepository(db)

    def get_stats(self) -> DashboardStats:
        return DashboardStats(
            total_notes=self.note_repo.count_by_user(self.user_id),
            pinned_notes=self.note_repo.count_pinned(self.user_id),
            total_tags=self.tag_repo.count_by_user(self.user_id),
            words_written=self.note_repo.count_words(self.user_id),
        )

    def get_recent_notes(self, limit: int = 6) -> list[Note]:
        return self.note_repo.get_recent(self.user_id, limit)

    def get_tags(self) -> list[Tag]:
        return self.tag_repo.get_by_user(self.user_id)
