"""Main menu inline keyboard shown after /start."""
from __future__ import annotations

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callbacks import GetMyLinkCb, SendMessageCb
from app.bot.texts import fa


def main_menu_keyboard(include_my_link: bool = True) -> InlineKeyboardMarkup:
    """Glass (inline) menu buttons.

    ``include_my_link`` is set False after the user has already fetched their
    link, so the button disappears and they can't tap it again (keeps the chat
    tidy and the message un-spammable).
    """
    builder = InlineKeyboardBuilder()
    if include_my_link:
        builder.button(text=fa.BTN_MY_LINK, callback_data=GetMyLinkCb())
    builder.button(text=fa.BTN_SEND_MESSAGE, callback_data=SendMessageCb())
    builder.adjust(1)
    return builder.as_markup()
