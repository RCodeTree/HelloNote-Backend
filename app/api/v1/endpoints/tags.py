"""标签路由（需登录）：列表与新建。"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.exceptions import ConflictError
from app.db.database import get_db
from app.models.user import User
from app.repositories.tag_repository import TagRepository
from app.schemas.note import TagCreate, TagPublic

router = APIRouter(prefix="/tags", tags=["tags"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[TagPublic])
def list_tags(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[TagPublic]:
    return TagRepository(db).get_by_user(user.id)


@router.post("", response_model=TagPublic, status_code=status.HTTP_201_CREATED)
def create_tag(
    data: TagCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TagPublic:
    repo = TagRepository(db)
    name = data.name.strip()
    if not name:
        raise ConflictError("标签名不能为空")
    if repo.get_by_name(user.id, name):
        raise ConflictError(f"标签「{name}」已存在")
    return repo.create(user_id=user.id, name=name, color=data.color)
