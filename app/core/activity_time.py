"""活跃度业务日工具。

统一以「可配置的固定 UTC 偏移」计算业务日（默认 UTC+8，等价 Asia/Shanghai），
不依赖 zoneinfo/tzdata（Windows 无系统时区库时也能稳定工作），
与 sql/v3 中 `stat_date DATE` 的口径保持一致。
"""
from datetime import date, datetime, timedelta, timezone

from app.core.config import get_settings


def _biz_timezone() -> timezone:
    return timezone(timedelta(hours=get_settings().activity_utc_offset_hours))


def business_today() -> date:
    """当前业务日（DATE，不含时分秒）。"""
    return datetime.now(_biz_timezone()).date()
