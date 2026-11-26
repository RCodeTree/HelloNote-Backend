"""笔友关系模型，映射到 hello_note.friendships 表（V5 新增）。"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, false, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UnsignedBigInt


class Friendship(Base):
    """笔友关系：请求方 requester -> 接收方 addressee，accept 后双向成为笔友。"""

    __tablename__ = "friendships"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    requester_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=False, index=True
    )
    addressee_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default="pending")
    # V6 好友设置：备注 / 可见范围 / 关系类别 / 关系程度
    note: Mapped[str | None] = mapped_column(String(100), nullable=True)
    privacy: Mapped[str] = mapped_column(String(16), nullable=False, server_default="all")
    relation_type: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default="friend"
    )
    closeness: Mapped[str] = mapped_column(
        String(16), nullable=False, server_default="friend"
    )
    # V7 好友置顶
    is_pinned: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("requester_id", "addressee_id", name="uk_friendships_pair"),
    )
