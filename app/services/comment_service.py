"""评论 / 点赞业务逻辑层：存在性与归属校验在此抛出业务异常。"""
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.comment import NoteComment
from app.models.note import Note
from app.repositories.comment_repository import CommentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.social import CommentCreate, LikeOut


class CommentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = CommentRepository(db)
        self.user_repo = UserRepository(db)

    # ---------- 评论 ----------
    def list_comments(self, note_id: int) -> list[NoteComment]:
        return self.repo.list_by_note(note_id)

    def create(self, note_id: int, user_id: int, data: CommentCreate) -> NoteComment:
        note = self.repo.get_note(note_id)
        if note is None:
            raise NotFoundError("笔记不存在")
        parent = None
        if data.parent_id is not None:
            parent = self.repo.get_by_id(data.parent_id)
            if parent is None or parent.note_id != note_id:
                raise NotFoundError("父评论不存在或不属于该笔记")
        comment = self.repo.create(note_id, user_id, data.content, data.parent_id)
        self._notify_on_comment(note, parent, user_id, data.content)
        return comment

    def _notify_on_comment(
        self, note: Note, parent: NoteComment | None, user_id: int, content: str
    ) -> None:
        """评论 / 回复通知埋点。

        - 回复（parent 存在）：通知被回复评论的作者（type=reply）
        - 顶级评论：通知笔记作者（type=comment）
        - 被回复者即笔记作者时，仅发 reply，避免同一人收到两条重复通知
        - 自己回复自己 / 自己评论自己：跳过
        通知失败不影响主业务（回滚仅丢弃通知事务，主评论已提交）。
        """
        try:
            from app.services.notification_service import NotificationService

            actor = self.user_repo.get_by_id(user_id)
            actor_name = actor.display_name if actor is not None else "有人"
            ns = NotificationService(self.db)
            notified: set[int] = set()

            # 1. 回复通知：发给被回复评论的作者
            if parent is not None and parent.user_id != user_id:
                ns.notify(
                    user_id=parent.user_id,
                    type="reply",
                    actor_id=user_id,
                    content=f"{actor_name}回复了你的评论：{content[:30]}",
                    related_id=note.id,
                )
                notified.add(parent.user_id)

            # 2. 笔记作者通知：仅当尚未通过 reply 通知到该作者
            if note.user_id != user_id and note.user_id not in notified:
                ns.notify(
                    user_id=note.user_id,
                    type="comment",
                    actor_id=user_id,
                    content=f"{actor_name}评论了你的笔记：{content[:30]}",
                    related_id=note.id,
                )
        except Exception:  # noqa: BLE001 - 通知失败不影响主业务
            self.db.rollback()

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
        note = self.repo.get_note(note_id)
        if note is None:
            raise NotFoundError("笔记不存在")
        like = self.repo.get_like(note_id, user_id)
        if like is None:
            self.repo.add_like(note_id, user_id)
            # 通知埋点：仅新增点赞时通知笔记作者（取消点赞不发）
            if note.user_id != user_id:
                try:
                    from app.services.notification_service import NotificationService

                    actor = self.user_repo.get_by_id(user_id)
                    actor_name = actor.display_name if actor is not None else "有人"
                    NotificationService(self.db).notify(
                        user_id=note.user_id,
                        type="like",
                        actor_id=user_id,
                        content=f"{actor_name}点赞了你的笔记",
                        related_id=note_id,
                    )
                except Exception:  # noqa: BLE001 - 通知失败不影响主业务；主业务已 commit，回滚仅丢弃本次通知事务
                    self.db.rollback()
        else:
            self.repo.remove_like(like)
        return self.get_like(note_id, user_id)
