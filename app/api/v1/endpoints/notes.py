"""笔记路由（需登录）。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.note import Note
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteOut

router = APIRouter(prefix="/notes", tags=["notes"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[NoteOut])
def list_notes(
    limit: int = 20,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[Note]:
    return NoteRepository(db).get_recent(user.id, limit)
