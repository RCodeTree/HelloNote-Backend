"""面板汇总路由（需登录）。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardStats
from app.schemas.note import NoteOut, TagPublic
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[Depends(get_current_user)])


@router.get("/stats", response_model=DashboardStats)
def get_stats(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> DashboardStats:
    return DashboardService(db, user.id).get_stats()


@router.get("/notes/recent", response_model=list[NoteOut])
def get_recent_notes(
    limit: int = 6,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Note]:
    return DashboardService(db, user.id).get_recent_notes(limit)


@router.get("/tags", response_model=list[TagPublic])
def get_tags(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> list[TagPublic]:
    return DashboardService(db, user.id).get_tags()
