"""用户相关响应模型。"""
from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    """对外暴露的用户信息（不含密码）。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    email: str
    avatar_url: str | None = None
    is_active: bool
