"""User business logic: registration, token rotation, settings."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.links.token_service import TokenService
from app.modules.users.models import User
from app.modules.users.repository import UserRepository


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = UserRepository(session)
        self._tokens = TokenService(self._repo)

    async def get_or_create(
        self, telegram_id: int, username: str | None
    ) -> tuple[User, bool]:
        """Return the user for a telegram id, creating one on first contact.

        Returns ``(user, created)``.
        """
        user = await self._repo.get_by_telegram_id(telegram_id)
        if user is not None:
            # Keep username fresh for support/debugging (not exposed to others).
            if username and user.username != username:
                user.username = username
            return user, False

        anonymous_id = await self._tokens.unique_anonymous_id()
        public_token = await self._tokens.unique_public_token()
        user = User(
            telegram_id=telegram_id,
            username=username,
            anonymous_id=anonymous_id,
            public_token=public_token,
        )
        await self._repo.add(user)
        return user, True

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._repo.get_by_id(user_id)

    async def get_by_public_token(self, token: str) -> User | None:
        return await self._repo.get_by_public_token(token)

    async def rotate_public_token(self, user: User) -> str:
        """Issue a fresh public token (invalidates the old deep link)."""
        user.public_token = await self._tokens.unique_public_token()
        await self._session.flush()
        return user.public_token

    async def set_seen_notifications(self, user: User, enabled: bool) -> None:
        user.seen_notifications_enabled = enabled
        await self._session.flush()
