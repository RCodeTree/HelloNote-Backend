"""活跃度数据访问层。

`add()` 使用 MySQL `INSERT ... ON DUPLICATE KEY UPDATE` 对唯一键
(user_id, stat_date) 做**原子累加**，天然支持并发且幂等安全。

重要：`add()` **不提交事务**，仅 `db.execute()`。由调用方在同一 Session 内
统一 commit —— 这样「笔记写入」与「活跃度累加」落在同一事务，不会出现
笔记成功但活跃度丢失的不一致（见 NoteRepository 的埋点）。
"""
from datetime import date

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.orm import Session

from app.models.activity import UserActivity


class ActivityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(
        self,
        user_id: int,
        stat_date: date,
        *,
        created: int = 0,
        updated: int = 0,
        deleted: int = 0,
        active_seconds: int = 0,
    ) -> None:
        """在当日行上原子累加计数 / 时长（不 commit）。"""
        stmt = mysql_insert(UserActivity).values(
            user_id=user_id,
            stat_date=stat_date,
            notes_created=created,
            notes_updated=updated,
            notes_deleted=deleted,
            active_seconds=active_seconds,
        )
        stmt = stmt.on_duplicate_key_update(
            notes_created=UserActivity.notes_created + stmt.inserted.notes_created,
            notes_updated=UserActivity.notes_updated + stmt.inserted.notes_updated,
            notes_deleted=UserActivity.notes_deleted + stmt.inserted.notes_deleted,
            active_seconds=UserActivity.active_seconds + stmt.inserted.active_seconds,
        )
        self.db.execute(stmt)

    def list_range(self, user_id: int, start: date, end: date) -> list[UserActivity]:
        stmt = (
            select(UserActivity)
            .where(
                UserActivity.user_id == user_id,
                UserActivity.stat_date >= start,
                UserActivity.stat_date <= end,
            )
            .order_by(UserActivity.stat_date.asc())
        )
        return list(self.db.execute(stmt).scalars().all())
