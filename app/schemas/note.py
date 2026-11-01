"""笔记与标签请求 / 响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


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


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(default="")
    is_pinned: bool = False
    tag_ids: list[int] = Field(default_factory=list)


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None
    is_pinned: bool | None = None
    tag_ids: list[int] | None = None
