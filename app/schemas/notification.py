"""系统通知的请求 / 响应模型（snake_case，供前端 api 层映射）。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    actor_id: int | None = None
    actor_name: str | None = None
    actor_avatar: str | None = None
    content: str
    related_id: int | None = None
    is_read: bool
    created_at: datetime


class UnreadCountOut(BaseModel):
    """未读通知数。"""

    count: int
