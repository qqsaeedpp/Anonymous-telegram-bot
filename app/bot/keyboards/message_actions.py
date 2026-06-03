"""Inline keyboard shown beneath a delivered anonymous message."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callbacks import BlockCb, ReplyCb, ViewCb
from app.bot.texts import fa


def message_actions_keyboard(
    message_id: int, conversation_id: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=fa.BTN_VIEW, callback_data=ViewCb(message_id=message_id))
    builder.button(
        text=fa.BTN_REPLY, callback_data=ReplyCb(conversation_id=conversation_id)
    )
    builder.button(
        text=fa.BTN_BLOCK, callback_data=BlockCb(conversation_id=conversation_id)
    )
    builder.adjust(1, 2)
    return builder.as_markup()


def seen_only_keyboard(
    conversation_id: int, blocked: bool
) -> InlineKeyboardMarkup:
    """Keyboard shown after a message has been viewed (reply + block/unblock)."""
    from app.bot.callbacks import UnblockCb

    builder = InlineKeyboardBuilder()
    builder.button(
        text=fa.BTN_REPLY, callback_data=ReplyCb(conversation_id=conversation_id)
    )
    if blocked:
        builder.button(
            text=fa.BTN_UNBLOCK,
            callback_data=UnblockCb(conversation_id=conversation_id),
        )
    else:
        builder.button(
            text=fa.BTN_BLOCK,
            callback_data=BlockCb(conversation_id=conversation_id),
        )
    builder.adjust(2)
    return builder.as_markup()


__all__ = [
    "message_actions_keyboard",
    "seen_only_keyboard",
    "InlineKeyboardButton",
]
