"""Application entrypoint.

Wires configuration, database, middlewares and routers, then starts polling.
Kept intentionally thin — no business logic lives here.
"""
from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import BotCommand

from app.bot.handlers import build_root_router
from app.bot.middlewares.db_session_middleware import DbSessionMiddleware
from app.bot.middlewares.error_middleware import ErrorMiddleware
from app.bot.middlewares.rate_limit_middleware import RateLimitMiddleware
from app.bot.middlewares.user_middleware import UserMiddleware
from app.config.bot_config import default_bot_properties
from app.config.settings import get_settings
from app.database.registry import create_all
from app.database.session import dispose_engine, init_engine
from app.modules.rate_limits.service import RateLimitService
from app.utils.logger import get_logger, setup_logging


async def run() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)
    logger = get_logger("main")

    # Database
    init_engine()
    # For MVP we auto-create tables; switch to Alembic migrations in production.
    await create_all()

    # Bot & dispatcher. Route through a proxy if configured (for blocked networks).
    session = AiohttpSession(proxy=settings.telegram_proxy) if settings.telegram_proxy else None
    if session is not None:
        logger.info("Using proxy for Telegram API.")
    bot = Bot(
        token=settings.bot_token,
        default=default_bot_properties(),
        session=session,
    )
    dp = Dispatcher()

    # Inject shared dependencies into handler data.
    dp["settings"] = settings

    rate_limiter = RateLimitService(
        max_messages=settings.rate_limit_max_messages,
        window_seconds=settings.rate_limit_window_seconds,
        cooldown_seconds=settings.rate_limit_cooldown_seconds,
    )

    # Middleware chain (outer -> inner).
    dp.update.outer_middleware(ErrorMiddleware())
    dp.update.outer_middleware(DbSessionMiddleware())
    dp.update.outer_middleware(UserMiddleware())
    dp.message.middleware(RateLimitMiddleware(rate_limiter))

    dp.include_router(build_root_router())

    logger.info("Bot starting (polling)...")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        # Register the /start command so it appears in Telegram's command menu.
        await bot.set_my_commands(
            [BotCommand(command="start", description="شروع کار با ربات")]
        )
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await dispose_engine()
        logger.info("Bot stopped.")


def main() -> None:
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
