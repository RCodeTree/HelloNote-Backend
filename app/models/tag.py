"""标签模型，映射到 hello_note.tags 表。"""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import UnsignedBigInt


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    notes: Mapped[list["Note"]] = relationship(  # noqa: F821
        "Note",
        secondary="note_tags",
        back_populates="tags",
        lazy="selectin",
    )
