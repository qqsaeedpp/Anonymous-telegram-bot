"""Data access for persistent user states."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.states.models import UserState


class StateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: int) -> UserState | None:
        return await self._session.get(UserState, user_id)

    async def upsert(
        self, user_id: int, state, context_json: str | None
    ) -> UserState:
        existing = await self._session.get(UserState, user_id)
        if existing is None:
            existing = UserState(
                user_id=user_id, state=state, context_json=context_json
            )
            self._session.add(existing)
        else:
            existing.state = state
            existing.context_json = context_json
        await self._session.flush()
        return existing
