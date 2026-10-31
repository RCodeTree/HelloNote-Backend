"""面板统计响应模型。"""
from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_notes: int
    pinned_notes: int
    total_tags: int
    words_written: int
