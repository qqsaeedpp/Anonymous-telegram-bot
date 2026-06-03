"""Two-step block confirmation keyboard."""
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callbacks import BlockCancelCb, BlockConfirmCb
from app.bot.texts import fa


def block_confirm_keyboard(conversation_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=fa.BTN_BLOCK_CONFIRM,
        callback_data=BlockConfirmCb(conversation_id=conversation_id),
    )
    builder.button(
        text=fa.BTN_BLOCK_CANCEL,
        callback_data=BlockCancelCb(conversation_id=conversation_id),
    )
    builder.adjust(2)
    return builder.as_markup()
