"""Anti-spam rate limiting for outgoing anonymous content.

Applied to plain text messages (the compose/reply inputs). Commands like
/start are exempt. Uses a shared in-memory RateLimitService.
"""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from app.bot.texts import fa
from app.modules.rate_limits.service import RateLimitService


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limiter: RateLimitService) -> None:
        self._limiter = limiter

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.text and not event.text.startswith("/"):
            user = data.get("user")
            if user is not None:
                decision = self._limiter.check(user.id, action="message")
                if not decision.allowed:
                    await event.answer(
                        fa.RATE_LIMITED.format(seconds=decision.retry_after)
                    )
                    return None
        return await handler(event, data)
