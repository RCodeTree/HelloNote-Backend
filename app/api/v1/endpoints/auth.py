"""认证路由：注册、登录、获取当前用户。"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin, UserRegister
from app.schemas.user import UserPublic, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)) -> User:
    return AuthService(db).register(data)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    user = AuthService(db).authenticate(data.account, data.password)
    if user is None:
        raise UnauthorizedError("用户名/邮箱或密码错误")
    token = create_access_token(user.id)
    return TokenResponse(access_token=token, user=UserPublic.model_validate(user))


@router.get("/me", response_model=UserPublic)
def read_me(user: User = Depends(get_current_user)) -> User:
    return user


@router.patch("/me", response_model=UserPublic)
def update_me(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """更新当前登录用户的昵称/头像。"""
    return AuthService(db).update_profile(user, data)
