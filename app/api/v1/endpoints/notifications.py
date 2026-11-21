"""系统通知路由（需登录）：列表 / 未读数 / 标已读 / 全部已读。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.notification import NotificationOut, UnreadCountOut
from app.schemas.social import OkOut
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[NotificationOut])
def list_notifications(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[NotificationOut]:
    return NotificationService(db).list_notifications(user.id)


@router.get("/unread-count", response_model=UnreadCountOut)
def unread_count(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UnreadCountOut:
    return NotificationService(db).unread_count(user.id)


@router.post("/read-all", response_model=OkOut)
def mark_all_read(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> OkOut:
    NotificationService(db).mark_all_read(user.id)
    return OkOut(ok=True)


@router.post("/{notification_id}/read", response_model=OkOut)
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> OkOut:
    NotificationService(db).mark_read(notification_id, user.id)
    return OkOut(ok=True)
