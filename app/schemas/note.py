"""笔记与标签请求 / 响应模型。"""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# 内容格式：markdown 需要 Markdown 解析（可预览），text 为纯文本
NoteFormat = Literal["markdown", "text"]


class TagPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    color: str | None = None


class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    color: str | None = Field(default=None, max_length=32)


class NoteOut(BaseModel):
    """单条笔记（含标签），用于列表 / 详情。前端负责将 content 截取为摘要。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    format: NoteFormat = "markdown"
    is_pinned: bool
    is_public: bool = False
    created_at: datetime
    updated_at: datetime
    tags: list[TagPublic] = []


class PublicNoteOut(BaseModel):
    """公开笔记（广场/笔友主页）：含作者信息与互动计数。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    excerpt: str
    format: NoteFormat = "markdown"
    author_id: int
    author_name: str
    author_avatar: str | None = None
    like_count: int = 0
    comment_count: int = 0
    created_at: datetime
    updated_at: datetime
    tags: list[TagPublic] = []


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(default="")
    format: NoteFormat = "markdown"
    is_pinned: bool = False
    is_public: bool = False
    tag_ids: list[int] = Field(default_factory=list)


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None
    format: NoteFormat | None = None
    is_pinned: bool | None = None
    is_public: bool | None = None
    tag_ids: list[int] | None = None
