"""活跃度业务逻辑层：心跳累加、范围聚合与汇总统计。

埋点说明：笔记增/改/删的计数写入放在 `NoteRepository` 的写方法内（与笔记
写入同一事务）；本服务负责「活动时长心跳」与「范围查询 / 汇总」。
"""
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.activity_time import business_today
from app.repositories.activity_repository import ActivityRepository
from app.schemas.activity import ActivityDay, ActivityRangeOut, ActivitySummary


class ActivityService:
    def __init__(self, db: Session, user_id: int) -> None:
        self.db = db
        self.user_id = user_id
        self.repo = ActivityRepository(db)

    def record_heartbeat(self, seconds: int, stat_date: date | None = None) -> date:
        """累加一段活跃时长并返回写入的业务日。"""
        day = stat_date or business_today()
        if seconds > 0:
            self.repo.add(self.user_id, day, active_seconds=seconds)
            self.db.commit()
        return day

    def get_range(self, days: int = 371) -> ActivityRangeOut:
        """返回最近 `days` 天的连续活跃度序列（含 0 值补齐）与汇总。

        days 默认 371（≈53 周），覆盖一整年的 GitHub 风格热力图；
        返回数组按日期升序，前端可直接铺日历 / 热力网格，无需自行补零。
        """
        days = max(7, min(days, 730))
        end = business_today()
        start = end - timedelta(days=days - 1)

        rows = self.repo.list_range(self.user_id, start, end)
        by_date = {r.stat_date: r for r in rows}

        day_list: list[ActivityDay] = []
        total_events = 0
        total_active_seconds = 0
        week_active_seconds = 0
        today_active_seconds = 0
        active_days = 0
        longest_streak = 0
        running = 0
        week_start = end - timedelta(days=6)

        cursor = start
        while cursor <= end:
            r = by_date.get(cursor)
            created = r.notes_created if r else 0
            updated = r.notes_updated if r else 0
            deleted = r.notes_deleted if r else 0
            seconds = r.active_seconds if r else 0
            count = created + updated + deleted

            day_list.append(
                ActivityDay(
                    date=cursor,
                    created=created,
                    updated=updated,
                    deleted=deleted,
                    count=count,
                    active_seconds=seconds,
                )
            )

            total_events += count
            total_active_seconds += seconds
            if cursor >= week_start:
                week_active_seconds += seconds
            if cursor == end:
                today_active_seconds = seconds

            # 活跃日：当日有点数或有活跃时长
            if count > 0 or seconds > 0:
                active_days += 1
                running += 1
                longest_streak = max(longest_streak, running)
            else:
                running = 0

            cursor += timedelta(days=1)

        # 当前连续活跃天数：从今天往回数，遇到非活跃日停止
        current_streak = 0
        cursor = end
        while cursor >= start:
            d = by_date.get(cursor)
            active = d is not None and (
                d.notes_created + d.notes_updated + d.notes_deleted > 0 or d.active_seconds > 0
            )
            if active:
                current_streak += 1
                cursor -= timedelta(days=1)
            else:
                break

        return ActivityRangeOut(
            start_date=start,
            end_date=end,
            days=day_list,
            summary=ActivitySummary(
                today_active_seconds=today_active_seconds,
                week_active_seconds=week_active_seconds,
                total_active_seconds=total_active_seconds,
                active_days=active_days,
                current_streak=current_streak,
                longest_streak=longest_streak,
                total_events=total_events,
            ),
        )
