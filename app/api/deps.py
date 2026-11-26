"""路由依赖：从 Bearer Token 解析当前登录用户。"""
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer = HTTPBearer(auto_error=False)

# 活跃时间写库节流：距上次记录超过该间隔才更新一次（避免高频轮询每请求写库）
ACTIVE_THROTTLE = timedelta(seconds=60)


def _touch_last_active(user: User, db: Session) -> None:
    """节流刷新用户最后活跃时间，支撑笔友在线状态展示。"""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    last = user.last_active_at
    if last is not None and (now - last) < ACTIVE_THROTTLE:
        return
    user.last_active_at = now
    db.commit()


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
    _touch_last_active(user, db)
    return user
