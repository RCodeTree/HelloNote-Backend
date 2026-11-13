"""每日活跃度模型，映射到 hello_note.user_activity 表（V3 新增）。"""
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import UnsignedBigInt


class UserActivity(Base):
    """用户每日活跃度：笔记 增/改/删 次数 + 活跃时长（秒）。

    一行代表「某用户某业务日」，由唯一键 (user_id, stat_date) 约束；
    写操作通过 MySQL `INSERT ... ON DUPLICATE KEY UPDATE` 原子累加。
    """

    __tablename__ = "user_activity"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    stat_date: Mapped[date] = mapped_column(Date, nullable=False)

    notes_created: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    notes_updated: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    notes_deleted: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    active_seconds: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("user_id", "stat_date", name="uk_user_activity_user_date"),
    )
