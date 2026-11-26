"""笔友关系数据访问层。commit / refresh 在本层完成。"""
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.models.friendship import Friendship
from app.models.user import User


class FriendshipRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, friendship_id: int) -> Friendship | None:
        return self.db.get(Friendship, friendship_id)

    def get_any_between(self, user1_id: int, user2_id: int) -> Friendship | None:
        """查询两人之间任意方向的关系记录。"""
        stmt = select(Friendship).where(
            or_(
                and_(
                    Friendship.requester_id == user1_id,
                    Friendship.addressee_id == user2_id,
                ),
                and_(
                    Friendship.requester_id == user2_id,
                    Friendship.addressee_id == user1_id,
                ),
            )
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_related(self, user_id: int, status: str) -> list[Friendship]:
        stmt = (
            select(Friendship)
            .where(
                or_(
                    Friendship.requester_id == user_id,
                    Friendship.addressee_id == user_id,
                ),
                Friendship.status == status,
            )
            .order_by(Friendship.is_pinned.desc(), Friendship.updated_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def search_users(
        self, q: str, exclude_ids: set[int], limit: int = 20
    ) -> list[User]:
        """按用户名 / 昵称模糊搜索，排除指定用户。"""
        like = f"%{q}%"
        stmt = select(User).where(
            or_(User.username.ilike(like), User.display_name.ilike(like))
        )
        if exclude_ids:
            stmt = stmt.where(User.id.notin_(exclude_ids))
        stmt = stmt.limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, requester_id: int, addressee_id: int) -> Friendship:
        friendship = Friendship(
            requester_id=requester_id, addressee_id=addressee_id, status="pending"
        )
        self.db.add(friendship)
        self.db.commit()
        self.db.refresh(friendship)
        return friendship

    def update_settings(
        self,
        friendship: Friendship,
        *,
        note: str | None = None,
        privacy: str | None = None,
        relation_type: str | None = None,
        closeness: str | None = None,
        is_pinned: bool | None = None,
    ) -> Friendship:
        """局部更新好友设置；未传（None）的字段保持不变，note 空串存 None。"""
        if note is not None:
            friendship.note = note or None
        if privacy is not None:
            friendship.privacy = privacy
        if relation_type is not None:
            friendship.relation_type = relation_type
        if closeness is not None:
            friendship.closeness = closeness
        if is_pinned is not None:
            friendship.is_pinned = is_pinned
        self.db.commit()
        self.db.refresh(friendship)
        return friendship

    def accept(self, friendship: Friendship) -> Friendship:
        friendship.status = "accepted"
        self.db.commit()
        self.db.refresh(friendship)
        return friendship

    def delete(self, friendship: Friendship) -> None:
        self.db.delete(friendship)
        self.db.commit()
