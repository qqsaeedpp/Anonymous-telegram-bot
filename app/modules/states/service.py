"""User FSM state management (persistent).

Context stores only ids — never message content — as a small JSON blob.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.states.models import UserStateKind
from app.modules.states.repository import StateRepository


@dataclass(frozen=True)
class CurrentState:
    kind: UserStateKind
    context: dict


class StateService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = StateRepository(session)

    async def get(self, user_id: int) -> CurrentState:
        row = await self._repo.get(user_id)
        if row is None:
            return CurrentState(kind=UserStateKind.IDLE, context={})
        context = json.loads(row.context_json) if row.context_json else {}
        return CurrentState(kind=row.state, context=context)

    async def set_waiting_for_target_username(self, user_id: int) -> None:
        await self._repo.upsert(
            user_id, UserStateKind.WAITING_FOR_TARGET_USERNAME, None
        )

    async def set_waiting_for_message(
        self, user_id: int, recipient_user_id: int
    ) -> None:
        """Target resolved (via link or username); now expect the message text."""
        await self._repo.upsert(
            user_id,
            UserStateKind.WAITING_FOR_ANONYMOUS_MESSAGE,
            json.dumps({"recipient_user_id": recipient_user_id}),
        )

    async def set_replying(self, user_id: int, conversation_id: int) -> None:
        await self._repo.upsert(
            user_id,
            UserStateKind.WAITING_FOR_REPLY,
            json.dumps({"conversation_id": conversation_id}),
        )

    async def clear(self, user_id: int) -> None:
        await self._repo.upsert(user_id, UserStateKind.IDLE, None)
