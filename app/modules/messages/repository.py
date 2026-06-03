"""Data access for messages."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.messages.models import Message


class MessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, message_id: int) -> Message | None:
        return await self._session.get(Message, message_id)

    async def add(self, message: Message) -> Message:
        self._session.add(message)
        await self._session.flush()
        return message
