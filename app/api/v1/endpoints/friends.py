"""笔友路由（需登录）：列表 / 请求 / 添加 / 接受 / 删除 / 搜索。"""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.social import AddFriendIn, FriendBrief, FriendOut, FriendSettingsIn, OkOut
from app.services.friendship_service import FriendshipService

router = APIRouter(prefix="/friends", tags=["friends"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[FriendOut])
def list_friends(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[FriendOut]:
    return FriendshipService(db).list_friends(user.id)


@router.get("/requests", response_model=list[FriendOut])
def list_requests(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[FriendOut]:
    return FriendshipService(db).list_requests(user.id)


@router.get("/search", response_model=list[FriendBrief])
def search_users(
    q: str = Query(min_length=1),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[FriendBrief]:
    return FriendshipService(db).search(user.id, q)


@router.post("", response_model=FriendOut, status_code=status.HTTP_201_CREATED)
def add_friend(
    data: AddFriendIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> FriendOut:
    return FriendshipService(db).add(user.id, data.username)


@router.post("/{friendship_id}/accept", response_model=FriendOut)
def accept_friend(
    friendship_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> FriendOut:
    return FriendshipService(db).accept(friendship_id, user.id)


@router.patch("/{friendship_id}/settings", response_model=FriendOut)
def update_friend_settings(
    friendship_id: int,
    data: FriendSettingsIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> FriendOut:
    return FriendshipService(db).update_settings(friendship_id, user.id, data)


@router.delete("/{friendship_id}", response_model=OkOut)
def delete_friend(
    friendship_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> OkOut:
    FriendshipService(db).delete(friendship_id, user.id)
    return OkOut(ok=True)
