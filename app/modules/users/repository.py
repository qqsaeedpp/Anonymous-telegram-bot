"""Data access for users."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self._session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def get_by_public_token(self, token: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.public_token == token)
        )
        return result.scalar_one_or_none()

    async def get_by_username_snapshot(self, normalized_username: str) -> User | None:
        """Case-insensitive lookup by stored Telegram username.

        ``normalized_username`` must already be lowercased and without ``@``.
        Only active members are matched. Returns the most recently updated match.
        """
        result = await self._session.execute(
            select(User)
            .where(
                func.lower(User.username_snapshot) == normalized_username,
                User.is_active.is_(True),
            )
            .order_by(User.updated_at.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def exists_anonymous_id(self, anonymous_id: str) -> bool:
        result = await self._session.execute(
            select(User.id).where(User.anonymous_id == anonymous_id)
        )
        return result.first() is not None

    async def exists_public_token(self, token: str) -> bool:
        result = await self._session.execute(
            select(User.id).where(User.public_token == token)
        )
        return result.first() is not None

    async def add(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        return user
