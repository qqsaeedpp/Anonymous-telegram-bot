"""Data access for blocks."""
from __future__ import annotations

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.blocks.models import Block


class BlockRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists(self, blocker_user_id: int, blocked_anonymous_id: str) -> bool:
        result = await self._session.execute(
            select(Block.id).where(
                Block.blocker_user_id == blocker_user_id,
                Block.blocked_anonymous_id == blocked_anonymous_id,
            )
        )
        return result.first() is not None

    async def add(self, block: Block) -> Block:
        self._session.add(block)
        await self._session.flush()
        return block

    async def remove(self, blocker_user_id: int, blocked_anonymous_id: str) -> None:
        await self._session.execute(
            delete(Block).where(
                Block.blocker_user_id == blocker_user_id,
                Block.blocked_anonymous_id == blocked_anonymous_id,
            )
        )
