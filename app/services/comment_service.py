"""评论 / 点赞业务逻辑层：存在性与归属校验在此抛出业务异常。"""
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.comment import NoteComment
from app.repositories.comment_repository import CommentRepository
from app.schemas.social import CommentCreate, LikeOut


class CommentService:
    def __init__(self, db: Session) -> None:
        self.repo = CommentRepository(db)

    # ---------- 评论 ----------
    def list_comments(self, note_id: int) -> list[NoteComment]:
        return self.repo.list_by_note(note_id)

    def create(self, note_id: int, user_id: int, data: CommentCreate) -> NoteComment:
        if self.repo.get_note(note_id) is None:
            raise NotFoundError("笔记不存在")
        if data.parent_id is not None:
            parent = self.repo.get_by_id(data.parent_id)
            if parent is None or parent.note_id != note_id:
                raise NotFoundError("父评论不存在或不属于该笔记")
        return self.repo.create(note_id, user_id, data.content, data.parent_id)

    def delete(self, comment_id: int, user_id: int) -> None:
        comment = self.repo.get_by_id(comment_id)
        if comment is None:
            raise NotFoundError("评论不存在")
        note = self.repo.get_note(comment.note_id)
        note_owner_id = note.user_id if note is not None else None
        if comment.user_id != user_id and note_owner_id != user_id:
            raise ForbiddenError("仅评论作者或笔记作者可删除该评论")
        self.repo.delete(comment)

    # ---------- 点赞 ----------
    def get_like(self, note_id: int, user_id: int) -> LikeOut:
        return LikeOut(
            like_count=self.repo.count_likes(note_id),
            liked_by_me=self.repo.get_like(note_id, user_id) is not None,
        )

    def toggle_like(self, note_id: int, user_id: int) -> LikeOut:
        if self.repo.get_note(note_id) is None:
            raise NotFoundError("笔记不存在")
        like = self.repo.get_like(note_id, user_id)
        if like is None:
            self.repo.add_like(note_id, user_id)
        else:
            self.repo.remove_like(like)
        return self.get_like(note_id, user_id)
