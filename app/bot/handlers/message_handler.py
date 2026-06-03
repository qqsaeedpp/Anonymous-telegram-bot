"""Catch-all text handler: routes plain text by the user's current state.

- COMPOSING -> create and deliver an anonymous message
- REPLYING  -> create and deliver a reply within a conversation
- IDLE      -> gentle hint
"""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.texts import fa
from app.config.settings import Settings
from app.modules.conversations.service import ConversationService
from app.modules.messages.schemas import SendOutcome
from app.modules.messages.service import MessageService
from app.modules.notifications.service import NotificationService
from app.modules.states.models import UserStateKind
from app.modules.states.service import StateService
from app.modules.users.models import User
from app.modules.users.service import UserService
from app.utils.text_sanitizer import is_blank

router = Router(name="messages")


async def _deliver(
    bot,
    session: AsyncSession,
    outcome: SendOutcome,
    is_reply: bool,
) -> None:
    target = await UserService(session).get_by_id(outcome.target_user_id)
    if target is None:
        return
    notifier = NotificationService(bot, MessageService(session))
    await notifier.deliver_message(outcome, target.telegram_id, is_reply=is_reply)


@router.message(F.text)
async def on_text(
    message: Message,
    bot,
    session: AsyncSession,
    user: User,
    settings: Settings,
) -> None:
    if is_blank(message.text):
        await message.answer(fa.EMPTY_MESSAGE)
        return

    states = StateService(session)
    current = await states.get(user.id)

    if current.kind == UserStateKind.COMPOSING:
        recipient_id = int(current.context.get("recipient_user_id", 0))
        recipient = await UserService(session).get_by_id(recipient_id)
        if recipient is None:
            await states.clear(user.id)
            await message.answer(fa.INVALID_LINK)
            return

        outcome = await MessageService(session).send_anonymous(
            recipient=recipient,
            sender=user,
            raw_text=message.text,
            max_length=settings.max_message_length,
        )
        await _deliver(bot, session, outcome, is_reply=False)
        await states.clear(user.id)
        await message.answer(fa.MESSAGE_SENT)
        return

    if current.kind == UserStateKind.REPLYING:
        conversation_id = int(current.context.get("conversation_id", 0))
        conversation = await ConversationService(session).get_by_id(conversation_id)
        if conversation is None:
            await states.clear(user.id)
            await message.answer(fa.CONVERSATION_NOT_FOUND)
            return

        outcome = await MessageService(session).send_reply(
            conversation=conversation,
            replier=user,
            raw_text=message.text,
            max_length=settings.max_message_length,
        )
        await _deliver(bot, session, outcome, is_reply=True)
        await states.clear(user.id)
        await message.answer(fa.REPLY_SENT)
        return

    await message.answer(fa.NOT_EXPECTING_MESSAGE)
