"""Aggregates all handler routers in registration order."""
from __future__ import annotations

from aiogram import Router

from app.bot.handlers import (
    block_handler,
    callback_handler,
    message_handler,
    reply_handler,
    start_handler,
)


def build_root_router() -> Router:
    root = Router()
    # Order matters: command + callback routers before the catch-all text router.
    root.include_router(start_handler.router)
    root.include_router(callback_handler.router)
    root.include_router(reply_handler.router)
    root.include_router(block_handler.router)
    root.include_router(message_handler.router)  # catch-all text last
    return root
