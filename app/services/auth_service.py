"""认证业务逻辑层。"""
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegister


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)

    def authenticate(self, account: str, password: str) -> User | None:
        """校验账号（用户名/邮箱）与密码，返回用户或 None。"""
        user = self.repo.get_by_account(account)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def register(self, data: UserRegister) -> User:
        if self.repo.get_by_username(data.username):
            raise ConflictError("用户名已被占用")
        if self.repo.get_by_email(data.email):
            raise ConflictError("该邮箱已注册")
        return self.repo.create(
            username=data.username,
            display_name=data.display_name,
            email=data.email,
            password_hash=hash_password(data.password),
        )
