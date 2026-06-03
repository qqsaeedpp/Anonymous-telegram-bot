"""Typed callback_data factories (aiogram CallbackData).

Only internal numeric ids travel in callback_data — never telegram_id, username
or public_token. Every handler must re-check ownership before acting (anti-IDOR).
"""
from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class GetMyLinkCb(CallbackData, prefix="get_my_link"):
    """Main-menu button: show the user's personal anonymous link."""


class SendMessageCb(CallbackData, prefix="send_message"):
    """Main-menu button: start the send-by-username flow."""


class ViewCb(CallbackData, prefix="view_message"):
    message_id: int


class ReplyCb(CallbackData, prefix="reply_message"):
    conversation_id: int


class BlockCb(CallbackData, prefix="block_request"):
    conversation_id: int


class BlockConfirmCb(CallbackData, prefix="block_confirm"):
    conversation_id: int


class BlockCancelCb(CallbackData, prefix="block_cancel"):
    conversation_id: int


class UnblockCb(CallbackData, prefix="unblock"):
    conversation_id: int


class SeenToggleCb(CallbackData, prefix="seen"):
    enable: int  # 1 = enable, 0 = disable
