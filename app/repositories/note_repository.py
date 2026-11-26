"""笔记数据访问层。"""
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.core.activity_time import business_today
from app.models.comment import NoteComment, NoteLike
from app.models.note import Note
from app.models.tag import Tag
from app.models.user import User
from app.repositories.activity_repository import ActivityRepository


class NoteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int, note_id: int) -> Note | None:
        stmt = (
            select(Note)
            .where(Note.id == note_id, Note.user_id == user_id)
            .options(selectinload(Note.tags))
        )
        return self.db.execute(stmt).scalars().first()

    def list_notes(
        self,
        user_id: int,
        *,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        tag_id: int | None = None,
    ) -> list[Note]:
        stmt = select(Note).where(Note.user_id == user_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Note.title.ilike(like), Note.content.ilike(like)))
        if tag_id is not None:
            stmt = stmt.join(Note.tags).where(Tag.id == tag_id)
        stmt = stmt.order_by(Note.is_pinned.desc(), Note.updated_at.desc())
        stmt = stmt.limit(limit).offset(offset).options(selectinload(Note.tags))
        return list(self.db.execute(stmt).scalars().all())

    def count_filtered(
        self,
        user_id: int,
        *,
        search: str | None = None,
        tag_id: int | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Note).where(Note.user_id == user_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Note.title.ilike(like), Note.content.ilike(like)))
        if tag_id is not None:
            stmt = stmt.join(Note.tags).where(Tag.id == tag_id)
        return int(self.db.execute(stmt).scalar_one())

    def count_by_user(self, user_id: int) -> int:
        stmt = select(func.count()).select_from(Note).where(Note.user_id == user_id)
        return int(self.db.execute(stmt).scalar_one())

    def count_pinned(self, user_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(Note)
            .where(Note.user_id == user_id, Note.is_pinned.is_(True))
        )
        return int(self.db.execute(stmt).scalar_one())

    def count_words(self, user_id: int) -> int:
        """累计字数（按字符数统计 content）。"""
        stmt = (
            select(func.coalesce(func.sum(func.char_length(Note.content)), 0))
            .select_from(Note)
            .where(Note.user_id == user_id)
        )
        return int(self.db.execute(stmt).scalar_one())

    def list_public(
        self,
        *,
        author_id: int | None = None,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        tag_id: int | None = None,
        sort: str = "hot",
    ) -> list[tuple[Note, str, str | None, int, int]]:
        """公开笔记列表（广场/笔友主页），附带作者与互动计数。

        返回 (note, author_name, author_avatar, like_count, comment_count)。
        计数用标量子查询一次算出，避免 N+1。
        """
        like_count = (
            select(func.count())
            .select_from(NoteLike)
            .where(NoteLike.note_id == Note.id)
            .scalar_subquery()
        )
        comment_count = (
            select(func.count())
            .select_from(NoteComment)
            .where(NoteComment.note_id == Note.id)
            .scalar_subquery()
        )
        stmt = (
            select(Note, User.display_name, User.avatar_url, like_count, comment_count)
            .join(User, User.id == Note.user_id)
            .where(Note.is_public.is_(True))
        )
        if author_id is not None:
            stmt = stmt.where(Note.user_id == author_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Note.title.ilike(like), Note.content.ilike(like)))
        if tag_id is not None:
            stmt = stmt.join(Note.tags).where(Tag.id == tag_id)
        if sort == "name":
            stmt = stmt.order_by(Note.title.asc(), Note.updated_at.desc())
        elif sort == "time":
            stmt = stmt.order_by(Note.updated_at.desc())
        else:  # hot：点赞权重更高 + 评论
            stmt = stmt.order_by((like_count * 2 + comment_count).desc(), Note.updated_at.desc())
        stmt = stmt.limit(limit).offset(offset).options(selectinload(Note.tags))
        rows = self.db.execute(stmt).all()
        return [(r[0], r[1], r[2], int(r[3]), int(r[4])) for r in rows]

    def count_public(
        self,
        *,
        author_id: int | None = None,
        search: str | None = None,
        tag_id: int | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Note).where(Note.is_public.is_(True))
        if author_id is not None:
            stmt = stmt.where(Note.user_id == author_id)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(or_(Note.title.ilike(like), Note.content.ilike(like)))
        if tag_id is not None:
            stmt = stmt.join(Note.tags).where(Tag.id == tag_id)
        return int(self.db.execute(stmt).scalar_one())

    def get_public_by_id(self, note_id: int) -> Note | None:
        stmt = (
            select(Note)
            .where(Note.id == note_id, Note.is_public.is_(True))
            .options(selectinload(Note.tags))
        )
        return self.db.execute(stmt).scalars().first()

    def get_recent(self, user_id: int, limit: int = 6) -> list[Note]:
        stmt = (
            select(Note)
            .where(Note.user_id == user_id)
            .options(selectinload(Note.tags))
            .order_by(Note.updated_at.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def create(
        self,
        user_id: int,
        *,
        title: str,
        content: str,
        is_pinned: bool,
        tag_ids: list[int],
        format: str = "markdown",
        is_public: bool = False,
    ) -> Note:
        note = Note(
            user_id=user_id, title=title, content=content, is_pinned=is_pinned,
            format=format, is_public=is_public,
        )
        self.db.add(note)
        self.db.flush()
        self._set_tags(note, user_id, tag_ids)
        # 活跃度埋点：新增 +1（同一事务，随笔记一起 commit）
        ActivityRepository(self.db).add(user_id, business_today(), created=1)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(
        self,
        note: Note,
        *,
        title: str | None = None,
        content: str | None = None,
        format: str | None = None,
        is_pinned: bool | None = None,
        is_public: bool | None = None,
        tag_ids: list[int] | None = None,
    ) -> Note:
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if format is not None:
            note.format = format
        if is_pinned is not None:
            note.is_pinned = is_pinned
        if is_public is not None:
            note.is_public = is_public
        if tag_ids is not None:
            self._set_tags(note, note.user_id, tag_ids)
        # 活跃度埋点：修改 +1（含 pin 置顶切换，因该路径同样调用 update）
        ActivityRepository(self.db).add(note.user_id, business_today(), updated=1)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, note: Note) -> None:
        # 活跃度埋点：删除 +1（先于物理删除，随后一起 commit）
        ActivityRepository(self.db).add(note.user_id, business_today(), deleted=1)
        self.db.delete(note)
        self.db.commit()

    def _set_tags(self, note: Note, user_id: int, tag_ids: list[int]) -> None:
        if not tag_ids:
            note.tags = []
            return
        tags = (
            self.db.execute(
                select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user_id)
            )
            .scalars()
            .all()
        )
        note.tags = list(tags)
