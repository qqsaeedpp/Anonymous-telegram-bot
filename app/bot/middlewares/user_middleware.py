"""Ensures the acting Telegram user exists in the DB and injects it."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser

from app.modules.users.service import UserService


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        tg_user: TgUser | None = data.get("event_from_user")
        session = data.get("session")
        if tg_user is not None and session is not None and not tg_user.is_bot:
            service = UserService(session)
            user, _ = await service.get_or_create(
                tg_user.id, tg_user.username, tg_user.first_name
            )
            data["user"] = user
        return await handler(event, data)
