"""路由依赖：从 Bearer Token 解析当前登录用户。"""
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    db: Session = Depends(get_db),
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> User:
    if creds is None or not creds.credentials:
        raise UnauthorizedError("缺少访问凭证")
    payload = decode_access_token(creds.credentials)
    if not payload or "sub" not in payload:
        raise UnauthorizedError("凭证无效或已过期")
    user = UserRepository(db).get_by_id(int(payload["sub"]))
    if user is None or not user.is_active:
        raise UnauthorizedError("用户不存在或已禁用")
    return user
