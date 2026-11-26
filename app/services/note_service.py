"""笔记业务逻辑层。"""
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteUpdate, PublicNoteOut, TagPublic


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
            is_public=data.is_public,
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
            is_public=data.is_public,
            tag_ids=data.tag_ids,
        )

    def delete(self, user_id: int, note_id: int) -> None:
        note = self.get(user_id, note_id)
        self.repo.delete(note)

    @staticmethod
    def _excerpt(content: str, limit: int = 120) -> str:
        text = " ".join((content or "").split())
        return text[:limit] + ("…" if len(text) > limit else "")

    @staticmethod
    def _to_public(
        note, author_name: str, author_avatar: str | None, like_count: int, comment_count: int
    ) -> PublicNoteOut:
        return PublicNoteOut(
            id=note.id,
            title=note.title,
            excerpt=NoteService._excerpt(note.content),
            format=note.format,
            author_id=note.user_id,
            author_name=author_name,
            author_avatar=author_avatar,
            like_count=like_count,
            comment_count=comment_count,
            created_at=note.created_at,
            updated_at=note.updated_at,
            tags=[TagPublic.model_validate(t) for t in note.tags],
        )

    def public_list(
        self,
        *,
        author_id: int | None = None,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        tag_id: int | None = None,
        sort: str = "hot",
    ) -> list[PublicNoteOut]:
        rows = self.repo.list_public(
            author_id=author_id, limit=limit, offset=offset,
            search=search, tag_id=tag_id, sort=sort,
        )
        return [self._to_public(*row) for row in rows]

    def public_count(
        self, *, author_id: int | None = None, search: str | None = None, tag_id: int | None = None
    ) -> int:
        return self.repo.count_public(author_id=author_id, search=search, tag_id=tag_id)

    def public_get(self, note_id: int) -> PublicNoteOut:
        note = self.repo.get_public_by_id(note_id)
        if note is None:
            raise NotFoundError("公开笔记不存在")
        author = self.repo.db.get(User, note.user_id)
        from app.repositories.comment_repository import CommentRepository

        comment_repo = CommentRepository(self.repo.db)
        return self._to_public(
            note,
            author.display_name if author else "匿名",
            author.avatar_url if author else None,
            comment_repo.count_likes(note_id),
            len(comment_repo.list_by_note(note_id)),
        )
