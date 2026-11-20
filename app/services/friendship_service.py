"""笔友业务逻辑层：存在性 / 归属 / 冲突校验在此抛出业务异常。"""
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.models.friendship import Friendship
from app.models.user import User
from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.user_repository import UserRepository
from app.schemas.social import FriendBrief, FriendOut


class FriendshipService:
    def __init__(self, db: Session) -> None:
        self.repo = FriendshipRepository(db)
        self.user_repo = UserRepository(db)

    @staticmethod
    def _peer_id(friendship: Friendship, me_id: int) -> int:
        return (
            friendship.addressee_id
            if friendship.requester_id == me_id
            else friendship.requester_id
        )

    @staticmethod
    def _to_out(friendship: Friendship, me_id: int, peer: User) -> FriendOut:
        return FriendOut(
            id=friendship.id,
            user_id=peer.id,
            username=peer.username,
            display_name=peer.display_name,
            avatar_url=peer.avatar_url,
            bio=peer.bio,
            status=friendship.status,
            is_requester=friendship.requester_id == me_id,
        )

    def _build_out(self, friendship: Friendship, me_id: int) -> FriendOut | None:
        peer = self.user_repo.get_by_id(self._peer_id(friendship, me_id))
        if peer is None:
            return None
        return self._to_out(friendship, me_id, peer)

    def list_friends(self, me_id: int) -> list[FriendOut]:
        result = []
        for fs in self.repo.list_related(me_id, "accepted"):
            out = self._build_out(fs, me_id)
            if out is not None:
                result.append(out)
        return result

    def list_requests(self, me_id: int) -> list[FriendOut]:
        result = []
        for fs in self.repo.list_related(me_id, "pending"):
            out = self._build_out(fs, me_id)
            if out is not None:
                result.append(out)
        return result

    def add(self, me_id: int, username: str) -> FriendOut:
        peer = self.user_repo.get_by_username(username)
        if peer is None:
            raise NotFoundError("用户不存在")
        if peer.id == me_id:
            raise ConflictError("不能添加自己为笔友")
        if self.repo.get_any_between(me_id, peer.id) is not None:
            raise ConflictError("笔友关系已存在")
        friendship = self.repo.create(me_id, peer.id)
        return self._to_out(friendship, me_id, peer)

    def accept(self, friendship_id: int, me_id: int) -> FriendOut:
        friendship = self.repo.get_by_id(friendship_id)
        if friendship is None:
            raise NotFoundError("好友请求不存在")
        if friendship.addressee_id != me_id:
            raise ForbiddenError("仅接收方可以接受该好友请求")
        friendship = self.repo.accept(friendship)
        out = self._build_out(friendship, me_id)
        if out is None:
            raise NotFoundError("用户不存在")
        return out

    def delete(self, friendship_id: int, me_id: int) -> None:
        friendship = self.repo.get_by_id(friendship_id)
        if friendship is None:
            raise NotFoundError("笔友关系不存在")
        if me_id not in (friendship.requester_id, friendship.addressee_id):
            raise ForbiddenError("无权删除该笔友关系")
        self.repo.delete(friendship)

    def search(self, me_id: int, q: str) -> list[FriendBrief]:
        exclude_ids = {me_id}
        for status in ("accepted", "pending"):
            for fs in self.repo.list_related(me_id, status):
                exclude_ids.add(self._peer_id(fs, me_id))
        users = self.repo.search_users(q, exclude_ids, limit=20)
        return [FriendBrief.model_validate(user) for user in users]
