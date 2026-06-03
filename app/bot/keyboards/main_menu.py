"""Main menu keyboard."""
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callbacks import SeenToggleCb
from app.bot.texts import fa


def main_menu_keyboard(seen_enabled: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=fa.BTN_TOGGLE_SEEN,
        callback_data=SeenToggleCb(enable=0 if seen_enabled else 1),
    )
    builder.adjust(1)
    return builder.as_markup()
