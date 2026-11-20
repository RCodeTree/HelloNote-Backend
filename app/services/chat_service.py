"""聊天业务逻辑层：会话参与者 / 笔友关系校验在此抛出业务异常。"""
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.chat import Conversation, Message
from app.repositories.chat_repository import ChatRepository
from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.user_repository import UserRepository
from app.schemas.social import ConversationOut, FriendBrief, MessageOut


class ChatService:
    def __init__(self, db: Session) -> None:
        self.repo = ChatRepository(db)
        self.friend_repo = FriendshipRepository(db)
        self.user_repo = UserRepository(db)

    @staticmethod
    def _peer_id(conversation: Conversation, me_id: int) -> int:
        return (
            conversation.user_b_id
            if conversation.user_a_id == me_id
            else conversation.user_a_id
        )

    def _to_conversation_out(
        self, conversation: Conversation, me_id: int
    ) -> ConversationOut:
        peer_id = self._peer_id(conversation, me_id)
        peer = self.user_repo.get_by_id(peer_id)
        brief = (
            FriendBrief.model_validate(peer)
            if peer is not None
            else FriendBrief(id=peer_id, username="", display_name="", avatar_url=None)
        )
        last = self.repo.get_last_message(conversation.id)
        return ConversationOut(
            id=conversation.id,
            peer=brief,
            last_message=last.content if last is not None else None,
            last_message_at=last.created_at.isoformat() if last is not None else None,
            unread_count=self.repo.count_unread(conversation.id, me_id),
            updated_at=conversation.updated_at,
        )

    @staticmethod
    def _require_participant(conversation: Conversation, me_id: int) -> None:
        if me_id not in (conversation.user_a_id, conversation.user_b_id):
            raise ForbiddenError("无权访问该会话")

    def list_conversations(self, me_id: int) -> list[ConversationOut]:
        return [
            self._to_conversation_out(c, me_id) for c in self.repo.list_for_user(me_id)
        ]

    def open_with(self, me_id: int, peer_id: int) -> ConversationOut:
        peer = self.user_repo.get_by_id(peer_id)
        if peer is None:
            raise NotFoundError("用户不存在")
        if peer_id == me_id:
            raise ForbiddenError("不能与自己开启会话")
        friendship = self.friend_repo.get_any_between(me_id, peer_id)
        if friendship is None or friendship.status != "accepted":
            raise ForbiddenError("仅笔友之间可以开启会话")
        low_id, high_id = sorted((me_id, peer_id))
        conversation = self.repo.get_by_pair(low_id, high_id)
        if conversation is None:
            conversation = self.repo.create_conversation(low_id, high_id)
        return self._to_conversation_out(conversation, me_id)

    def list_messages(self, conversation_id: int, me_id: int) -> list[MessageOut]:
        conversation = self.repo.get_conversation(conversation_id)
        if conversation is None:
            raise NotFoundError("会话不存在")
        self._require_participant(conversation, me_id)
        messages = self.repo.list_messages(conversation_id)
        self.repo.mark_read(conversation_id, me_id)
        return [MessageOut.model_validate(message) for message in messages]

    def send_message(self, conversation_id: int, me_id: int, content: str) -> MessageOut:
        conversation = self.repo.get_conversation(conversation_id)
        if conversation is None:
            raise NotFoundError("会话不存在")
        self._require_participant(conversation, me_id)
        message = self.repo.create_message(conversation, me_id, content)
        return MessageOut.model_validate(message)
