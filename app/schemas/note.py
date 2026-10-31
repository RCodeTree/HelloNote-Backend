"""笔记与标签响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TagPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    color: str | None = None


class NoteOut(BaseModel):
    """单条笔记（含标签），用于列表 / 详情。前端负责将 content 截取为摘要。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    is_pinned: bool
    created_at: datetime
    updated_at: datetime
    tags: list[TagPublic] = []
