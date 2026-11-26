"""笔记路由（需登录）。支持列表 / 新建 / 详情 / 更新 / 置顶切换 / 删除。"""
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteOut, NoteUpdate, PublicNoteOut
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


# ===== V10 公开笔记：广场 / 笔友主页（须在 /{note_id} 之前，避免被当整数 id 匹配）=====
@router.get("/public", response_model=list[PublicNoteOut])
def list_public_notes(
    response: Response,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str | None = Query(default=None),
    tag_id: int | None = Query(default=None),
    sort: str = Query("hot", pattern="^(hot|name|time)$"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[PublicNoteOut]:
    service = NoteService(db)
    notes = service.public_list(limit=limit, offset=offset, search=search, tag_id=tag_id, sort=sort)
    response.headers["X-Total-Count"] = str(service.public_count(search=search, tag_id=tag_id))
    return notes


@router.get("/public/{note_id}", response_model=PublicNoteOut)
def get_public_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PublicNoteOut:
    return NoteService(db).public_get(note_id)


@router.get("/users/{author_id}/public", response_model=list[PublicNoteOut])
def list_user_public_notes(
    author_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[PublicNoteOut]:
    return NoteService(db).public_list(author_id=author_id, limit=limit, offset=offset)


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
