"""Main-menu button handlers: "get my link" and "send message".

"get my link" shows the user's personal deep link (only the public_token is in
the link — never telegram_id or anonymous_id). "send message" starts the
send-by-username flow by moving the user into WAITING_FOR_TARGET_USERNAME.
"""
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.callbacks import GetMyLinkCb, SendMessageCb
from app.bot.texts import fa
from app.config.settings import Settings
from app.modules.states.service import StateService
from app.modules.users.models import User
from app.modules.users.service import UserService

router = Router(name="menu")


@router.callback_query(GetMyLinkCb.filter())
async def on_get_my_link(
    query: CallbackQuery,
    session: AsyncSession,
    user: User,
    settings: Settings,
) -> None:
    # Ensure a public token exists (it always should), then build the link.
    if not user.public_token:
        await UserService(session).rotate_public_token(user)
    link = settings.deep_link(user.public_token)
    await query.message.answer(fa.your_link(link))
    await query.answer()


@router.callback_query(SendMessageCb.filter())
async def on_send_message(
    query: CallbackQuery,
    session: AsyncSession,
    user: User,
) -> None:
    await StateService(session).set_waiting_for_target_username(user.id)
    await query.message.answer(fa.ASK_TARGET_USERNAME)
    await query.answer()
