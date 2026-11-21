"""系统通知模型，映射到 hello_note.notifications 表（V6 新增）。"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import UnsignedBigInt

if TYPE_CHECKING:
    from app.models.user import User


class Notification(Base):
    """通知：user_id 为接收者，actor_id 为触发者（可空，如系统通知）。"""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        UnsignedBigInt,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type: Mapped[str] = mapped_column(String(24), nullable=False)
    actor_id: Mapped[int | None] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=True
    )
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    related_id: Mapped[int | None] = mapped_column(UnsignedBigInt, nullable=True)
    is_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), index=True
    )

    # 触发者资料；两张表间存在 user_id / actor_id 两条外键路径，需显式指定。
    # 系统通知 actor_id 为 None，此时属性返回 None。
    actor: Mapped["User | None"] = relationship(
        "User", foreign_keys=[actor_id], lazy="selectin"
    )

    @property
    def actor_name(self) -> str | None:
        return self.actor.display_name if self.actor is not None else None

    @property
    def actor_avatar(self) -> str | None:
        return self.actor.avatar_url if self.actor is not None else None
