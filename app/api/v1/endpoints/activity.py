"""活跃度路由（需登录）：范围查询 + 心跳上报。"""
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.activity import ActivityRangeOut, HeartbeatIn, HeartbeatOut
from app.services.activity_service import ActivityService

router = APIRouter(prefix="/activity", tags=["activity"], dependencies=[Depends(get_current_user)])


@router.get("/range", response_model=ActivityRangeOut)
def get_activity_range(
    days: int = Query(371, ge=7, le=730),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ActivityRangeOut:
    """返回最近 days 天的每日活跃度（日历 / 热力图 / 活动时长共用）。"""
    return ActivityService(db, user.id).get_range(days)


@router.post("/heartbeat", response_model=HeartbeatOut)
def post_heartbeat(
    data: HeartbeatIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> HeartbeatOut:
    """前端心跳：累加一段活跃时长（秒）。"""
    day: date = ActivityService(db, user.id).record_heartbeat(data.active_seconds, data.date)
    return HeartbeatOut(date=day, active_seconds=data.active_seconds)
