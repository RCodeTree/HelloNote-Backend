"""笔记业务逻辑层。"""
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, db: Session) -> None:
        self.repo = NoteRepository(db)

    def list(
        self,
        user_id: int,
        *,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        tag_id: int | None = None,
    ) -> list:
        return self.repo.list_notes(
            user_id, limit=limit, offset=offset, search=search, tag_id=tag_id
        )

    def count(self, user_id: int, *, search: str | None = None, tag_id: int | None = None) -> int:
        return self.repo.count_filtered(user_id, search=search, tag_id=tag_id)

    def get(self, user_id: int, note_id: int):
        note = self.repo.get_by_id(user_id, note_id)
        if note is None:
            raise NotFoundError("笔记不存在")
        return note

    def create(self, user_id: int, data: NoteCreate):
        return self.repo.create(
            user_id,
            title=data.title,
            content=data.content,
            format=data.format,
            is_pinned=data.is_pinned,
            tag_ids=data.tag_ids,
        )

    def update(self, user_id: int, note_id: int, data: NoteUpdate):
        note = self.get(user_id, note_id)
        return self.repo.update(
            note,
            title=data.title,
            content=data.content,
            format=data.format,
            is_pinned=data.is_pinned,
            tag_ids=data.tag_ids,
        )

    def delete(self, user_id: int, note_id: int) -> None:
        note = self.get(user_id, note_id)
        self.repo.delete(note)
