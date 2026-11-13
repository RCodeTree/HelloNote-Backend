"""活跃度相关的请求 / 响应模型（snake_case，供前端 api 层映射）。"""
from datetime import date as DateType

from pydantic import BaseModel, Field


class ActivityDay(BaseModel):
    """某业务日的活跃度明细。"""

    date: DateType
    created: int = 0
    updated: int = 0
    deleted: int = 0
    # 当日活跃点数 = created + updated + deleted（热力图颜色深浅依据）
    count: int = 0
    # 当日活跃时长（秒）
    active_seconds: int = 0


class ActivitySummary(BaseModel):
    """活跃度汇总（用于「活动时长」等统计卡片）。"""

    today_active_seconds: int = 0
    week_active_seconds: int = 0
    total_active_seconds: int = 0
    active_days: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    total_events: int = 0


class ActivityRangeOut(BaseModel):
    """范围查询结果：连续日期序列 + 汇总。"""

    start_date: DateType
    end_date: DateType
    days: list[ActivityDay] = Field(default_factory=list)
    summary: ActivitySummary = Field(default_factory=ActivitySummary)


class HeartbeatIn(BaseModel):
    """前端心跳：上报一段增量活跃时长（秒）。

    date 可选：前端可显式指定业务日；缺省则由后端按当前业务日计算。
    """

    active_seconds: int = Field(default=0, ge=0, le=3600)
    date: DateType | None = None


class HeartbeatOut(BaseModel):
    date: DateType
    active_seconds: int
