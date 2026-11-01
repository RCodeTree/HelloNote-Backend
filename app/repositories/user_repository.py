"""用户数据访问层。"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_account(self, account: str) -> User | None:
        """支持用户名或邮箱登录。"""
        stmt = select(User).where(
            (User.username == account) | (User.email == account)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def count(self) -> int:
        stmt = select(func.count()).select_from(User)
        return int(self.db.execute(stmt).scalar_one())

    def create(
        self,
        *,
        username: str,
        display_name: str,
        email: str,
        password_hash: str,
    ) -> User:
        user = User(
            username=username,
            display_name=display_name,
            email=email,
            password_hash=password_hash,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(
        self,
        user: User,
        *,
        display_name: str | None = None,
        avatar_url: str | None = None,
    ) -> User:
        """局部更新用户资料；未传入的字段不修改。avatar_url 传空串表示清除。"""
        if display_name is not None:
            user.display_name = display_name
        if avatar_url is not None:
            user.avatar_url = avatar_url or None
        self.db.commit()
        self.db.refresh(user)
        return user
