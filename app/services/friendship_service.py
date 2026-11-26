"""笔友业务逻辑层：存在性 / 归属 / 冲突校验在此抛出业务异常。"""
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.models.friendship import Friendship
from app.models.user import User
from app.repositories.chat_repository import ChatRepository
from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.user_repository import UserRepository
from app.schemas.social import FriendBrief, FriendOut, FriendSettingsIn


class FriendshipService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = FriendshipRepository(db)
        self.user_repo = UserRepository(db)
        self.chat_repo = ChatRepository(db)

    @staticmethod
    def _peer_id(friendship: Friendship, me_id: int) -> int:
        return (
            friendship.addressee_id
            if friendship.requester_id == me_id
            else friendship.requester_id
        )

    @staticmethod
    def _to_out(
        friendship: Friendship, me_id: int, peer: User, unread_count: int = 0
    ) -> FriendOut:
        return FriendOut(
            id=friendship.id,
            user_id=peer.id,
            username=peer.username,
            display_name=peer.display_name,
            avatar_url=peer.avatar_url,
            bio=peer.bio,
            status=friendship.status,
            is_requester=friendship.requester_id == me_id,
            note=friendship.note,
            privacy=friendship.privacy or "all",
            relation_type=friendship.relation_type or "friend",
            closeness=friendship.closeness or "friend",
            is_pinned=friendship.is_pinned,
            unread_count=unread_count,
        )

    def _count_unread_from_peer(self, me_id: int, peer_id: int) -> int:
        """统计该笔友发给当前用户的未读消息数（复用会话仓库）。"""
        low_id, high_id = sorted((me_id, peer_id))
        conversation = self.chat_repo.get_by_pair(low_id, high_id)
        if conversation is None:
            return 0
        return self.chat_repo.count_unread(conversation.id, me_id)

    def _build_out(self, friendship: Friendship, me_id: int) -> FriendOut | None:
        peer_id = self._peer_id(friendship, me_id)
        peer = self.user_repo.get_by_id(peer_id)
        if peer is None:
            return None
        return self._to_out(
            friendship, me_id, peer, self._count_unread_from_peer(me_id, peer_id)
        )

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
        # 通知埋点：给接收方发好友申请通知（失败不影响主业务）
        try:
            from app.services.notification_service import NotificationService

            actor = self.user_repo.get_by_id(me_id)
            actor_name = actor.display_name if actor is not None else "有人"
            NotificationService(self.db).notify(
                user_id=peer.id,
                type="friend_request",
                actor_id=me_id,
                content=f"{actor_name}申请添加你为笔友",
                related_id=friendship.id,
            )
        except Exception:  # noqa: BLE001 - 通知失败不影响主业务；主业务已 commit，回滚仅丢弃本次通知事务
            self.db.rollback()
        return self._to_out(friendship, me_id, peer)

    def accept(self, friendship_id: int, me_id: int) -> FriendOut:
        friendship = self.repo.get_by_id(friendship_id)
        if friendship is None:
            raise NotFoundError("好友请求不存在")
        if friendship.addressee_id != me_id:
            raise ForbiddenError("仅接收方可以接受该好友请求")
        requester_id = friendship.requester_id
        friendship = self.repo.accept(friendship)
        # 通知埋点：给申请方发接受通知（失败不影响主业务）
        try:
            from app.services.notification_service import NotificationService

            actor = self.user_repo.get_by_id(me_id)
            actor_name = actor.display_name if actor is not None else "有人"
            NotificationService(self.db).notify(
                user_id=requester_id,
                type="friend_accept",
                actor_id=me_id,
                content=f"{actor_name}接受了你的笔友申请",
                related_id=friendship.id,
            )
        except Exception:  # noqa: BLE001 - 通知失败不影响主业务；主业务已 commit，回滚仅丢弃本次通知事务
            self.db.rollback()
        out = self._build_out(friendship, me_id)
        if out is None:
            raise NotFoundError("用户不存在")
        return out

    def update_settings(
        self, friendship_id: int, me_id: int, data: FriendSettingsIn
    ) -> FriendOut:
        friendship = self.repo.get_by_id(friendship_id)
        if friendship is None:
            raise NotFoundError("笔友关系不存在")
        if me_id not in (friendship.requester_id, friendship.addressee_id):
            raise ForbiddenError("无权修改该笔友关系设置")
        self.repo.update_settings(
            friendship,
            note=data.note,
            privacy=data.privacy,
            relation_type=data.relation_type,
            closeness=data.closeness,
            is_pinned=data.is_pinned,
        )
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
