"""系统通知数据访问层。commit / refresh 在本层完成。"""
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session, selectinload

from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, notification_id: int) -> Notification | None:
        return self.db.get(Notification, notification_id)

    def create(
        self,
        *,
        user_id: int,
        type: str,
        actor_id: int | None = None,
        content: str,
        related_id: int | None = None,
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            type=type,
            actor_id=actor_id,
            content=content,
            related_id=related_id,
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def list_for_user(self, user_id: int, limit: int = 100) -> list[Notification]:
        """当前用户通知，按创建时间倒序，最多 limit 条。"""
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .options(selectinload(Notification.actor))
        )
        return list(self.db.execute(stmt).scalars().all())

    def count_unread(self, user_id: int) -> int:
        stmt = select(func.count()).select_from(Notification).where(
            Notification.user_id == user_id,
            Notification.is_read.is_(False),
        )
        return int(self.db.execute(stmt).scalar_one())

    def count_by_type(self, user_id: int, type: str) -> int:
        """按类型计数（供种子幂等判重）。"""
        stmt = select(func.count()).select_from(Notification).where(
            Notification.user_id == user_id,
            Notification.type == type,
        )
        return int(self.db.execute(stmt).scalar_one())

    def mark_read(self, notification: Notification) -> Notification:
        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_all_read(self, user_id: int) -> None:
        stmt = (
            update(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .values(is_read=True)
        )
        self.db.execute(stmt)
        self.db.commit()

    def seed_system_notification(self, user_id: int, content: str) -> None:
        """幂等插入系统欢迎通知：该用户尚无 system 类型通知时才写入。"""
        if self.count_by_type(user_id, "system") > 0:
            return
        self.create(user_id=user_id, type="system", content=content)
