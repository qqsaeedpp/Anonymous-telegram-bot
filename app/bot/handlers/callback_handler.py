"""Callback for viewing ("seeing") an anonymous message.

The recipient receives only a notification + a single "view" button. Pressing
it reveals the text (edited in place), swaps in the after-view keyboard, and —
only the first time — notifies the author that their message was seen.
"""
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.callbacks import ViewCb
from app.bot.keyboards.message_actions import after_view_keyboard
from app.bot.texts import fa
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
    result = await MessageService(session).view(callback_data.message_id, user)

    # ``None`` means the viewer is not the rightful owner (anti-IDOR) or the
    # message/conversation vanished. Stay silent about details.
    if result is None:
        await query.answer(fa.CONVERSATION_NOT_FOUND, show_alert=True)
        return

    # Reveal the text in place, then offer reply (+ block for the recipient).
    body = fa.revealed_message(
        sender_label=result.author_label,
        text=result.safe_text,
        is_reply=result.is_reply,
    )
    keyboard = after_view_keyboard(
        conversation_id=result.conversation_id,
        can_block=result.viewer_is_recipient,
        blocked=result.is_blocked,
    )
    try:
        await query.message.edit_text(body, reply_markup=keyboard)
    except Exception:  # noqa: BLE001 - edit may fail if content is unchanged
        pass

    # Notify the author exactly once, and only if they opted in.
    if result.should_notify_seen:
        author = await UserService(session).get_by_id(result.author_user_id)
        if author is not None and author.seen_notifications_enabled:
            notifier = NotificationService(bot, MessageService(session))
            await notifier.notify_seen(author.telegram_id)

    await query.answer(fa.MESSAGE_SEEN_ACK)
