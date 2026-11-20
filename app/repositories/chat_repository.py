"""会话 / 消息数据访问层。commit / refresh 在本层完成。"""
from sqlalchemy import func, or_, select, update
from sqlalchemy.orm import Session

from app.models.chat import Conversation, Message


class ChatRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # ---------- 会话 ----------
    def get_conversation(self, conversation_id: int) -> Conversation | None:
        return self.db.get(Conversation, conversation_id)

    def get_by_pair(self, low_id: int, high_id: int) -> Conversation | None:
        stmt = select(Conversation).where(
            Conversation.user_low_id == low_id, Conversation.user_high_id == high_id
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_for_user(self, user_id: int) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .where(
                or_(
                    Conversation.user_a_id == user_id,
                    Conversation.user_b_id == user_id,
                )
            )
            .order_by(Conversation.updated_at.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def create_conversation(self, low_id: int, high_id: int) -> Conversation:
        conversation = Conversation(
            user_a_id=low_id,
            user_b_id=high_id,
            user_low_id=low_id,
            user_high_id=high_id,
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    # ---------- 消息 ----------
    def list_messages(self, conversation_id: int) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_last_message(self, conversation_id: int) -> Message | None:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalars().first()

    def count_unread(self, conversation_id: int, user_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.sender_id != user_id,
                Message.is_read.is_(False),
            )
        )
        return int(self.db.execute(stmt).scalar_one())

    def mark_read(self, conversation_id: int, user_id: int) -> None:
        """把会话中对方发来的未读消息标记为已读。"""
        stmt = (
            update(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.sender_id != user_id,
                Message.is_read.is_(False),
            )
            .values(is_read=True)
        )
        self.db.execute(stmt)
        self.db.commit()

    def create_message(
        self, conversation: Conversation, sender_id: int, content: str
    ) -> Message:
        message = Message(
            conversation_id=conversation.id, sender_id=sender_id, content=content
        )
        self.db.add(message)
        # touch 会话更新时间（onupdate 亦会生效）
        conversation.updated_at = func.now()
        self.db.commit()
        self.db.refresh(message)
        return message
