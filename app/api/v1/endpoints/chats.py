"""聊天路由（需登录）：会话列表 / 开启会话 / 消息列表 / 发送消息。"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.social import ConversationOut, MessageCreate, MessageOut, OkOut
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chats", tags=["chats"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[ConversationOut])
def list_chats(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[ConversationOut]:
    return ChatService(db).list_conversations(user.id)


@router.post("/with/{user_id}", response_model=ConversationOut)
def open_chat(
    user_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ConversationOut:
    return ChatService(db).open_with(user.id, user_id)


@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
def list_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[MessageOut]:
    return ChatService(db).list_messages(conversation_id, user.id)


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageOut,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    conversation_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MessageOut:
    return ChatService(db).send_message(conversation_id, user.id, data.content)


@router.post("/{conversation_id}/read", response_model=OkOut)
def mark_read(
    conversation_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> OkOut:
    ChatService(db).mark_read(conversation_id, user.id)
    return OkOut(ok=True)
