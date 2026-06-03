"""Block business logic with idempotent block/unblock and snapshot sync."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.blocks.models import Block
from app.modules.blocks.repository import BlockRepository
from app.modules.conversations.models import Conversation
from app.modules.conversations.service import ConversationService


class BlockService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = BlockRepository(session)
        self._conversations = ConversationService(session)

    async def is_blocked(
        self, blocker_user_id: int, blocked_anonymous_id: str
    ) -> bool:
        return await self._repo.exists(blocker_user_id, blocked_anonymous_id)

    async def block_from_conversation(self, conversation: Conversation) -> None:
        """Block the sender of a conversation (idempotent)."""
        already = await self._repo.exists(
            conversation.recipient_user_id, conversation.sender_anonymous_id
        )
        if not already:
            await self._repo.add(
                Block(
                    blocker_user_id=conversation.recipient_user_id,
                    blocked_anonymous_id=conversation.sender_anonymous_id,
                )
            )
        await self._conversations.set_blocked_snapshot(conversation, True)

    async def unblock_from_conversation(self, conversation: Conversation) -> None:
        await self._repo.remove(
            conversation.recipient_user_id, conversation.sender_anonymous_id
        )
        await self._conversations.set_blocked_snapshot(conversation, False)
