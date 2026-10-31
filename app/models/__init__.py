"""模型包：导入以注册所有映射与关联表到 Base.metadata。"""
from app.models.note import Note
from app.models.note_tag import note_tags
from app.models.tag import Tag
from app.models.user import User

__all__ = ["User", "Tag", "Note", "note_tags"]
