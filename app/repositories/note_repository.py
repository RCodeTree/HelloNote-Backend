"""笔记数据访问层。"""
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.note import Note
from app.models.tag import Tag


class NoteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int, note_id: int) -> Note | None:
        stmt = (
            select(Note)
            .where(Note.id == note_id, Note.user_id == user_id)
            .options(selectinload(Note.tags))
        )
        return self.db.execute(stmt).scalars().first()

    def list_notes(
        self,
        user_id: int,
        *,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        tag_id: int | None = None,
    ) -> list[Note]:
        stmt = select(Note).where(Note.user_id == user_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Note.title.ilike(like), Note.content.ilike(like)))
        if tag_id is not None:
            stmt = stmt.join(Note.tags).where(Tag.id == tag_id)
        stmt = stmt.order_by(Note.is_pinned.desc(), Note.updated_at.desc())
        stmt = stmt.limit(limit).offset(offset).options(selectinload(Note.tags))
        return list(self.db.execute(stmt).scalars().all())

    def count_filtered(
        self,
        user_id: int,
        *,
        search: str | None = None,
        tag_id: int | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Note).where(Note.user_id == user_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Note.title.ilike(like), Note.content.ilike(like)))
        if tag_id is not None:
            stmt = stmt.join(Note.tags).where(Tag.id == tag_id)
        return int(self.db.execute(stmt).scalar_one())

    def get_recent(self, user_id: int, limit: int = 6) -> list[Note]:
        stmt = (
            select(Note)
            .where(Note.user_id == user_id)
            .options(selectinload(Note.tags))
            .order_by(Note.updated_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def create(
        self,
        user_id: int,
        *,
        title: str,
        content: str,
        is_pinned: bool,
        tag_ids: list[int],
    ) -> Note:
        note = Note(user_id=user_id, title=title, content=content, is_pinned=is_pinned)
        self.db.add(note)
        self.db.flush()
        self._set_tags(note, user_id, tag_ids)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(
        self,
        note: Note,
        *,
        title: str | None = None,
        content: str | None = None,
        is_pinned: bool | None = None,
        tag_ids: list[int] | None = None,
    ) -> Note:
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if is_pinned is not None:
            note.is_pinned = is_pinned
        if tag_ids is not None:
            self._set_tags(note, note.user_id, tag_ids)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, note: Note) -> None:
        self.db.delete(note)
        self.db.commit()

    def _set_tags(self, note: Note, user_id: int, tag_ids: list[int]) -> None:
        if not tag_ids:
            note.tags = []
            return
        tags = (
            self.db.execute(
                select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user_id)
            )
            .scalars()
            .all()
        )
        note.tags = list(tags)
