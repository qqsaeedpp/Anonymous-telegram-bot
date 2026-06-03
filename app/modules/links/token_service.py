"""Generation of collision-free unique tokens/ids backed by the user table."""
from __future__ import annotations

from app.modules.users.repository import UserRepository
from app.utils.id_generator import generate_anonymous_id
from app.utils.token_generator import generate_public_token

_MAX_ATTEMPTS = 10


class TokenService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def unique_anonymous_id(self) -> str:
        for _ in range(_MAX_ATTEMPTS):
            candidate = generate_anonymous_id()
            if not await self._repo.exists_anonymous_id(candidate):
                return candidate
        raise RuntimeError("Could not generate a unique anonymous_id")

    async def unique_public_token(self) -> str:
        for _ in range(_MAX_ATTEMPTS):
            candidate = generate_public_token()
            if not await self._repo.exists_public_token(candidate):
                return candidate
        raise RuntimeError("Could not generate a unique public_token")
