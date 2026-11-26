"""笔友个人设置数据访问层。commit / refresh 在本层完成。"""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.friend_setting import FriendSetting
from app.models.friendship import Friendship


class FriendSettingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_settings(self, friendship_id: int, user_id: int) -> FriendSetting | None:
        stmt = select(FriendSetting).where(
            FriendSetting.friendship_id == friendship_id,
            FriendSetting.user_id == user_id,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_or_create_settings(self, friendship_id: int, user_id: int) -> FriendSetting:
        """查不到则创建默认行；并发插入冲突时回滚后重查。"""
        settings = self.get_settings(friendship_id, user_id)
        if settings is not None:
            return settings
        settings = FriendSetting(friendship_id=friendship_id, user_id=user_id)
        self.db.add(settings)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            existing = self.get_settings(friendship_id, user_id)
            if existing is None:
                raise
            return existing
        self.db.refresh(settings)
        return settings

    def update_settings(
        self,
        friendship: Friendship,
        me_id: int,
        *,
        note: str | None = None,
        privacy: str | None = None,
        relation_type: str | None = None,
        closeness: str | None = None,
        is_pinned: bool | None = None,
    ) -> FriendSetting:
        """局部更新当前用户的个人设置；None 字段不改，note 空串存 None。"""
        settings = self.get_or_create_settings(friendship.id, me_id)
        if note is not None:
            settings.note = note or None
        if privacy is not None:
            settings.privacy = privacy
        if relation_type is not None:
            settings.relation_type = relation_type
        if closeness is not None:
            settings.closeness = closeness
        if is_pinned is not None:
            settings.is_pinned = is_pinned
        self.db.commit()
        self.db.refresh(settings)
        return settings
