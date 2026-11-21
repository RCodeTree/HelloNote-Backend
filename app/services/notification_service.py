"""系统通知业务逻辑层：归属校验在此抛出业务异常。"""
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.repositories.notification_repo import NotificationRepository
from app.schemas.notification import NotificationOut, UnreadCountOut


class NotificationService:
    def __init__(self, db: Session) -> None:
        self.repo = NotificationRepository(db)

    def list_notifications(self, user_id: int) -> list[NotificationOut]:
        return [
            NotificationOut.model_validate(item)
            for item in self.repo.list_for_user(user_id, limit=100)
        ]

    def unread_count(self, user_id: int) -> UnreadCountOut:
        return UnreadCountOut(count=self.repo.count_unread(user_id))

    def mark_read(self, notification_id: int, user_id: int) -> None:
        notification = self.repo.get_by_id(notification_id)
        if notification is None:
            raise NotFoundError("通知不存在")
        if notification.user_id != user_id:
            raise ForbiddenError("无权操作该通知")
        self.repo.mark_read(notification)

    def mark_all_read(self, user_id: int) -> None:
        self.repo.mark_all_read(user_id)

    def notify(
        self,
        user_id: int,
        type: str,
        actor_id: int | None,
        content: str,
        related_id: int | None = None,
    ) -> NotificationOut:
        """统一通知入口：仅新增一条通知（db.add + commit 由仓库完成）。"""
        notification = self.repo.create(
            user_id=user_id,
            type=type,
            actor_id=actor_id,
            content=content,
            related_id=related_id,
        )
        return NotificationOut.model_validate(notification)
