"""Catches unhandled errors, logs them, and shows a generic message."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.bot.texts import fa
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ErrorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:  # noqa: BLE001 - top-level safety net
            logger.exception("Unhandled error while processing update")
            try:
                inner = getattr(event, "event", event)
                if isinstance(inner, Message):
                    await inner.answer(fa.GENERIC_ERROR)
                elif isinstance(inner, CallbackQuery):
                    await inner.answer(fa.GENERIC_ERROR, show_alert=True)
            except Exception:  # noqa: BLE001
                pass
            return None
