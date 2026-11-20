"""评论与点赞模型，映射到 hello_note.note_comments / note_likes 表（V5 新增）。"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import UnsignedBigInt

if TYPE_CHECKING:
    from app.models.user import User


class NoteComment(Base):
    """笔记评论：parent_id 指向父评论，支持一层 / 多层回复。"""

    __tablename__ = "note_comments"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    note_id: Mapped[int] = mapped_column(
        UnsignedBigInt,
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=False, index=True
    )
    parent_id: Mapped[int | None] = mapped_column(
        UnsignedBigInt,
        ForeignKey("note_comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    author: Mapped["User"] = relationship("User", lazy="selectin")

    @property
    def author_name(self) -> str:
        return self.author.display_name

    @property
    def author_avatar(self) -> str | None:
        return self.author.avatar_url


class NoteLike(Base):
    """笔记点赞：同一用户对同一笔记仅能有一条记录。"""

    __tablename__ = "note_likes"

    id: Mapped[int] = mapped_column(UnsignedBigInt, primary_key=True, autoincrement=True)
    note_id: Mapped[int] = mapped_column(
        UnsignedBigInt,
        ForeignKey("notes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        UnsignedBigInt, ForeignKey("users.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("note_id", "user_id", name="uk_note_likes_note_user"),
    )
