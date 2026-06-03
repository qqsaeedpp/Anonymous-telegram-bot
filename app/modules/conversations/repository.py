"""Data access for conversations."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.conversations.models import Conversation


class ConversationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, conversation_id: int) -> Conversation | None:
        return await self._session.get(Conversation, conversation_id)

    async def get_pair(
        self, recipient_user_id: int, sender_user_id: int
    ) -> Conversation | None:
        result = await self._session.execute(
            select(Conversation).where(
                Conversation.recipient_user_id == recipient_user_id,
                Conversation.sender_user_id == sender_user_id,
            )
        )
        return result.scalar_one_or_none()

    async def add(self, conversation: Conversation) -> Conversation:
        self._session.add(conversation)
        await self._session.flush()
        return conversation
