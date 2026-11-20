"""评论 / 点赞数据访问层。commit / refresh 在本层完成。"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.comment import NoteComment, NoteLike
from app.models.note import Note


class CommentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # ---------- 笔记 ----------
    def get_note(self, note_id: int) -> Note | None:
        return self.db.get(Note, note_id)

    # ---------- 评论 ----------
    def list_by_note(self, note_id: int) -> list[NoteComment]:
        stmt = (
            select(NoteComment)
            .where(NoteComment.note_id == note_id)
            .order_by(NoteComment.created_at.asc())
            .options(selectinload(NoteComment.author))
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_by_id(self, comment_id: int) -> NoteComment | None:
        stmt = (
            select(NoteComment)
            .where(NoteComment.id == comment_id)
            .options(selectinload(NoteComment.author))
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def create(
        self, note_id: int, user_id: int, content: str, parent_id: int | None = None
    ) -> NoteComment:
        comment = NoteComment(
            note_id=note_id, user_id=user_id, content=content, parent_id=parent_id
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: NoteComment) -> None:
        self.db.delete(comment)
        self.db.commit()

    # ---------- 点赞 ----------
    def get_like(self, note_id: int, user_id: int) -> NoteLike | None:
        stmt = select(NoteLike).where(
            NoteLike.note_id == note_id, NoteLike.user_id == user_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def count_likes(self, note_id: int) -> int:
        stmt = select(func.count()).select_from(NoteLike).where(NoteLike.note_id == note_id)
        return int(self.db.execute(stmt).scalar_one())

    def add_like(self, note_id: int, user_id: int) -> None:
        self.db.add(NoteLike(note_id=note_id, user_id=user_id))
        self.db.commit()

    def remove_like(self, like: NoteLike) -> None:
        self.db.delete(like)
        self.db.commit()
