"""/start handlers: plain start and deep-link start."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.main_menu import main_menu_keyboard
from app.bot.texts import fa
from app.config.settings import Settings
from app.modules.links.service import LinkService
from app.modules.states.service import StateService
from app.modules.users.models import User

router = Router(name="start")


async def _send_main_menu(message: Message) -> None:
    """Welcome text + the two glass (inline) buttons."""
    await message.answer(fa.WELCOME, reply_markup=main_menu_keyboard())


@router.message(CommandStart(deep_link=True))
async def start_with_deep_link(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    user: User,
    settings: Settings,
) -> None:
    token = command.args or ""
    resolution = await LinkService(session).resolve(token)

    if not resolution.is_valid or resolution.recipient is None:
        await message.answer(fa.INVALID_LINK)
        await _send_main_menu(message)
        return

    recipient = resolution.recipient
    if recipient.id == user.id:
        await message.answer(fa.CANNOT_MESSAGE_SELF)
        await _send_main_menu(message)
        return

    await StateService(session).set_waiting_for_message(user.id, recipient.id)
    await message.answer(fa.compose_prompt(recipient.anonymous_id))


@router.message(CommandStart())
async def start_plain(
    message: Message,
    session: AsyncSession,
    user: User,
    settings: Settings,
) -> None:
    await StateService(session).clear(user.id)
    await _send_main_menu(message)
