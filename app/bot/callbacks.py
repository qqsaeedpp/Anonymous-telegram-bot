"""Typed callback_data factories (aiogram CallbackData).

Only internal numeric ids travel in callback_data — never telegram_id or
public_token. Every handler must re-check ownership before acting (anti-IDOR).
"""
from __future__ import annotations

from aiogram.filters.callback_data import CallbackData


class ViewCb(CallbackData, prefix="view"):
    message_id: int


class ReplyCb(CallbackData, prefix="rep"):
    conversation_id: int


class BlockCb(CallbackData, prefix="blk"):
    conversation_id: int


class BlockConfirmCb(CallbackData, prefix="blkY"):
    conversation_id: int


class BlockCancelCb(CallbackData, prefix="blkN"):
    conversation_id: int


class UnblockCb(CallbackData, prefix="unblk"):
    conversation_id: int


class SeenToggleCb(CallbackData, prefix="seen"):
    enable: int  # 1 = enable, 0 = disable
