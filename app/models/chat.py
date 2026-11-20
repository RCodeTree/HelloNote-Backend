"""会话与消息模型，映射到 hello_note.conversations / messages 表（V5 新增）。"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UnsignedBigInt


class Conversation(Base):
    """笔友会话：user_low_id / user_high_id 为归一化后的用户 id，保证 A-B 与 B-A 唯一。"""

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    user_a_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=False, index=True
    )
    user_b_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=False, index=True
    )
    user_low_id: Mapped[int] = mapped_column(UnsignedBigInt, nullable=False, index=True)
    user_high_id: Mapped[int] = mapped_column(UnsignedBigInt, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("user_low_id", "user_high_id", name="uk_conversations_pair"),
    )


class Message(Base):
    """会话消息。"""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(
        UnsignedBigInt,
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sender_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(String(2000), nullable=False)
    is_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), index=True
    )
