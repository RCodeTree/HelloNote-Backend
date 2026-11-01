"""笔记路由（需登录）。支持列表 / 新建 / 详情 / 更新 / 置顶切换 / 删除。"""
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteOut, NoteUpdate
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[NoteOut])
def list_notes(
    response: Response,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str | None = Query(default=None),
    tag_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[NoteOut]:
    service = NoteService(db)
    notes = service.list(user.id, limit=limit, offset=offset, search=search, tag_id=tag_id)
    total = service.count(user.id, search=search, tag_id=tag_id)
    response.headers["X-Total-Count"] = str(total)
    return notes


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> NoteOut:
    return NoteService(db).create(user.id, data)


@router.get("/{note_id}", response_model=NoteOut)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> NoteOut:
    return NoteService(db).get(user.id, note_id)


@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    data: NoteUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> NoteOut:
    return NoteService(db).update(user.id, note_id, data)


@router.patch("/{note_id}/pin", response_model=NoteOut)
def toggle_pin(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> NoteOut:
    service = NoteService(db)
    note = service.get(user.id, note_id)
    return NoteRepository(db).update(note, is_pinned=not note.is_pinned)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Response:
    NoteService(db).delete(user.id, note_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
