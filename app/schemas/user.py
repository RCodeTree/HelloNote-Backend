"""用户相关响应模型。"""
from pydantic import BaseModel, ConfigDict, Field


class UserPublic(BaseModel):
    """对外暴露的用户信息（不含密码）。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    email: str
    avatar_url: str | None = None
    is_active: bool


class UserUpdate(BaseModel):
    """更新当前用户资料（字段可选，未提供则不修改）。

    avatar_url 传空字符串表示清除头像。
    """

    display_name: str | None = Field(default=None, min_length=1, max_length=100)
    avatar_url: str | None = Field(default=None, max_length=500)
