"""评论 / 点赞 / 笔友 / 聊天 请求与响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------- 评论 ----------
class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
    parent_id: int | None = None


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    note_id: int
    user_id: int
    author_name: str
    author_avatar: str | None = None
    parent_id: int | None = None
    content: str
    created_at: datetime


# ---------- 点赞 ----------
class LikeOut(BaseModel):
    like_count: int
    liked_by_me: bool


# ---------- 笔友 ----------
class FriendBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    avatar_url: str | None = None


class FriendOut(BaseModel):
    """对方的信息 + 关系状态；id 为关系 id，user_id 为对方用户 id。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    username: str
    display_name: str
    avatar_url: str | None = None
    bio: str | None = None
    status: str
    is_requester: bool
    # V6 好友设置（来自 friendships 表）
    note: str | None = None
    privacy: str = "all"
    relation_type: str = "friend"
    closeness: str = "friend"
    # 对方发给当前用户的未读消息数
    unread_count: int = 0


# 好友请求与好友列表结构一致，直接复用
FriendRequestOut = FriendOut


class AddFriendIn(BaseModel):
    username: str = Field(min_length=1, max_length=50)


class FriendSettingsIn(BaseModel):
    """好友设置局部更新：全部可选，None 表示不修改。"""

    note: str | None = Field(default=None, max_length=100)
    privacy: str | None = Field(default=None, max_length=16)
    relation_type: str | None = Field(default=None, max_length=32)
    closeness: str | None = Field(default=None, max_length=16)


# ---------- 聊天 ----------
class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    sender_id: int
    content: str
    is_read: bool
    created_at: datetime


class ConversationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    peer: FriendBrief
    last_message: str | None = None
    last_message_at: str | None = None
    unread_count: int
    updated_at: datetime


class OkOut(BaseModel):
    """删除类接口统一返回体。"""

    ok: bool
