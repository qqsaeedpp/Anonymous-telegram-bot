"""Callbacks for viewing a message (seen) and toggling seen notifications."""
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.callbacks import SeenToggleCb, ViewCb
from app.bot.keyboards.main_menu import main_menu_keyboard
from app.bot.keyboards.message_actions import seen_only_keyboard
from app.bot.texts import fa
from app.modules.blocks.service import BlockService
from app.modules.conversations.service import ConversationService
from app.modules.messages.models import MessageDirection
from app.modules.messages.service import MessageService
from app.modules.notifications.service import NotificationService
from app.modules.users.models import User
from app.modules.users.service import UserService

router = Router(name="callbacks")


@router.callback_query(ViewCb.filter())
async def on_view(
    query: CallbackQuery,
    callback_data: ViewCb,
    bot,
    session: AsyncSession,
    user: User,
) -> None:
    message = await MessageService(session).mark_seen(callback_data.message_id, user)

    if message is not None:
        conversation = await ConversationService(session).get_by_id(
            message.conversation_id
        )
        if conversation is not None:
            # The author of this message is the one to be notified of "seen".
            if message.direction == MessageDirection.TO_RECIPIENT:
                author_id = conversation.sender_user_id
            else:
                author_id = conversation.recipient_user_id

            author = await UserService(session).get_by_id(author_id)
            if author is not None and author.seen_notifications_enabled:
                notifier = NotificationService(bot, MessageService(session))
                await notifier.notify_seen(author.telegram_id)

            blocked = await BlockService(session).is_blocked(
                user.id, conversation.sender_anonymous_id
            )
            try:
                await query.message.edit_reply_markup(
                    reply_markup=seen_only_keyboard(conversation.id, blocked)
                )
            except Exception:  # noqa: BLE001 - markup may be unchanged
                pass

    await query.answer(fa.MESSAGE_SEEN_ACK)


@router.callback_query(SeenToggleCb.filter())
async def on_toggle_seen(
    query: CallbackQuery,
    callback_data: SeenToggleCb,
    session: AsyncSession,
    user: User,
) -> None:
    enabled = bool(callback_data.enable)
    await UserService(session).set_seen_notifications(user, enabled)
    try:
        await query.message.edit_reply_markup(
            reply_markup=main_menu_keyboard(enabled)
        )
    except Exception:  # noqa: BLE001
        pass
    await query.answer(fa.seen_setting_status(enabled))
