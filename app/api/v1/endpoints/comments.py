"""评论 / 点赞路由（需登录）。所有人可读评论，写操作按契约校验。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.social import CommentCreate, CommentOut, LikeOut, OkOut
from app.services.comment_service import CommentService

router = APIRouter(prefix="/comments", tags=["comments"], dependencies=[Depends(get_current_user)])


@router.get("/notes/{note_id}/comments", response_model=list[CommentOut])
def list_comments(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[CommentOut]:
    return CommentService(db).list_comments(note_id)


@router.post("/notes/{note_id}/comments", response_model=CommentOut)
def create_comment(
    note_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CommentOut:
    return CommentService(db).create(note_id, user.id, data)


@router.delete("/comments/{comment_id}", response_model=OkOut)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> OkOut:
    CommentService(db).delete(comment_id, user.id)
    return OkOut(ok=True)


@router.get("/notes/{note_id}/like", response_model=LikeOut)
def get_like(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LikeOut:
    return CommentService(db).get_like(note_id, user.id)


@router.post("/notes/{note_id}/like", response_model=LikeOut)
def toggle_like(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LikeOut:
    return CommentService(db).toggle_like(note_id, user.id)
