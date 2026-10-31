"""笔记-标签关联表（复合主键），不映射为独立模型，供 ORM 关系 secondary 引用。"""
from sqlalchemy import Column, ForeignKey, Table

from app.db.base import Base
from app.db.types import UnsignedBigInt

note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", UnsignedBigInt, ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", UnsignedBigInt, ForeignKey("tags.id"), primary_key=True),
)
