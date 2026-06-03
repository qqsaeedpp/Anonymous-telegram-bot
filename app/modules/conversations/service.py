"""Conversation business logic: thread creation and lookup."""
from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.conversations.models import Conversation
from app.modules.conversations.repository import ConversationRepository
from app.modules.users.models import User


class ConversationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = ConversationRepository(session)

    async def get_or_create(
        self, recipient: User, sender: User
    ) -> Conversation:
        """Return the thread between sender and recipient, creating if needed."""
        conv = await self._repo.get_pair(recipient.id, sender.id)
        if conv is not None:
            return conv
        conv = Conversation(
            recipient_user_id=recipient.id,
            sender_user_id=sender.id,
            sender_anonymous_id=sender.anonymous_id,
        )
        return await self._repo.add(conv)

    async def get_by_id(self, conversation_id: int) -> Conversation | None:
        return await self._repo.get_by_id(conversation_id)

    async def touch(self, conversation: Conversation) -> None:
        """Bump the last_message_at marker."""
        conversation.last_message_at = func.now()
        await self._session.flush()

    async def set_blocked_snapshot(
        self, conversation: Conversation, blocked: bool
    ) -> None:
        conversation.is_blocked = blocked
        await self._session.flush()
