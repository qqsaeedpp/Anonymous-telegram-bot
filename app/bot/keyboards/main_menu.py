"""Main menu inline keyboard shown after /start."""
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callbacks import GetMyLinkCb, SendMessageCb
from app.bot.texts import fa


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Two glass (inline) buttons: get my link / send a message."""
    builder = InlineKeyboardBuilder()
    builder.button(text=fa.BTN_MY_LINK, callback_data=GetMyLinkCb())
    builder.button(text=fa.BTN_SEND_MESSAGE, callback_data=SendMessageCb())
    builder.adjust(1)
    return builder.as_markup()
