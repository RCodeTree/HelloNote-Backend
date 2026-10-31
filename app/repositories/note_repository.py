"""笔记数据访问层。"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.note import Note


class NoteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_recent(self, user_id: int, limit: int = 6) -> list[Note]:
        stmt = (
            select(Note)
            .where(Note.user_id == user_id)
            .options(selectinload(Note.tags))
            .order_by(Note.updated_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_by_user(self, user_id: int) -> int:
        stmt = select(func.count()).select_from(Note).where(Note.user_id == user_id)
        return int(self.db.execute(stmt).scalar_one())

    def count_pinned(self, user_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(Note)
            .where(Note.user_id == user_id, Note.is_pinned.is_(True))
        )
        return int(self.db.execute(stmt).scalar_one())

    def count_words(self, user_id: int) -> int:
        """累计字数（按字符数统计 content）。"""
        stmt = (
            select(func.coalesce(func.sum(func.char_length(Note.content)), 0))
            .select_from(Note)
            .where(Note.user_id == user_id)
        )
        return int(self.db.execute(stmt).scalar_one())
