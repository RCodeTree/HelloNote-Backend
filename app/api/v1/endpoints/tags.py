"""标签路由（需登录）。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.tag_repository import TagRepository
from app.schemas.note import TagPublic

router = APIRouter(prefix="/tags", tags=["tags"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[TagPublic])
def list_tags(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[TagPublic]:
    return TagRepository(db).get_by_user(user.id)
