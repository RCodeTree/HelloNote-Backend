"""笔友个人设置模型，映射到 hello_note.friend_settings 表。

备注 / 隐私 / 关系类别 / 亲密程度 / 置顶均为「用户个人行为」：
一条笔友关系（friendships 行）对应双方各自独立的一行 friend_settings。
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, false, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UnsignedBigInt


class FriendSetting(Base):
    """某个用户对某条笔友关系的个人设置（(friendship_id, user_id) 唯一）。"""

    __tablename__ = "friend_settings"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    friendship_id: Mapped[int] = mapped_column(
        UnsignedBigInt,
        ForeignKey("friendships.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        UnsignedBigInt,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    note: Mapped[str | None] = mapped_column(String(100), nullable=True)
    privacy: Mapped[str] = mapped_column(String(16), nullable=False, server_default="all")
    relation_type: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default="friend"
    )
    closeness: Mapped[str] = mapped_column(
        String(16), nullable=False, server_default="friend"
    )
    is_pinned: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("friendship_id", "user_id", name="uk_fs_pair"),
    )
