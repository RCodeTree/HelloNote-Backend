"""标签数据访问层。"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.tag import Tag


class TagRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_user(self, user_id: int) -> list[Tag]:
        stmt = select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        return list(self.db.execute(stmt).scalars().all())

    def count_by_user(self, user_id: int) -> int:
        stmt = select(func.count()).select_from(Tag).where(Tag.user_id == user_id)
        return int(self.db.execute(stmt).scalar_one())
