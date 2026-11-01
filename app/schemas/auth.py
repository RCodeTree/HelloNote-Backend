"""认证相关请求 / 响应模型。"""
from pydantic import BaseModel, Field

from app.schemas.user import UserPublic


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    display_name: str = Field(min_length=1, max_length=100)
    # 轻量邮箱格式校验（避免引入 email-validator 依赖）
    email: str = Field(max_length=255, pattern=r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    # 用户名或邮箱，二选一登录
    account: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
