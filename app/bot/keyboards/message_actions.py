"""Inline keyboards for delivered anonymous messages.

- ``view_only_keyboard``: shown on arrival — a single "view" button. The text
  is hidden until the recipient presses it.
- ``after_view_keyboard``: shown after viewing — reply, plus block/unblock for
  the conversation recipient only.
"""
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callbacks import BlockCb, ReplyCb, UnblockCb, ViewCb
from app.bot.texts import fa


def view_only_keyboard(message_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=fa.BTN_VIEW, callback_data=ViewCb(message_id=message_id))
    builder.adjust(1)
    return builder.as_markup()


def after_view_keyboard(
    conversation_id: int, can_block: bool, blocked: bool
) -> InlineKeyboardMarkup:
    """Keyboard shown after a message has been viewed."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text=fa.BTN_REPLY, callback_data=ReplyCb(conversation_id=conversation_id)
    )
    if can_block:
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


__all__ = ["view_only_keyboard", "after_view_keyboard"]
