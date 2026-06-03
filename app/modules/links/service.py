"""Deep-link resolution: token -> recipient user."""
from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User
from app.modules.users.repository import UserRepository


@dataclass(frozen=True)
class LinkResolution:
    recipient: User | None
    is_valid: bool


class LinkService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserRepository(session)

    async def resolve(self, token: str) -> LinkResolution:
        """Resolve a public token to its owner (the message recipient)."""
        token = (token or "").strip()
        if not token:
            return LinkResolution(recipient=None, is_valid=False)
        user = await self._repo.get_by_public_token(token)
        return LinkResolution(recipient=user, is_valid=user is not None)
