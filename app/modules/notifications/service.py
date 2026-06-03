"""Delivery of messages and notifications to Telegram chats.

This is the only service that talks to the Telegram Bot API. It translates
domain outcomes into outgoing messages and keeps message records in sync
(e.g. storing the delivered telegram_message_id).
"""
from __future__ import annotations

from aiogram import Bot

from app.bot.keyboards.message_actions import message_actions_keyboard
from app.bot.texts import fa
from app.modules.messages.schemas import SendOutcome
from app.modules.messages.service import MessageService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class NotificationService:
    def __init__(self, bot: Bot, message_service: MessageService) -> None:
        self._bot = bot
        self._messages = message_service

    async def deliver_message(
        self, outcome: SendOutcome, target_telegram_id: int, is_reply: bool
    ) -> None:
        """Deliver a new message/reply to the target's chat, with action buttons."""
        if not outcome.delivered:
            # Target has blocked the sender. Silently drop (no leak to sender).
            return

        header = fa.NEW_REPLY_HEADER if is_reply else fa.NEW_MESSAGE_HEADER
        body = fa.incoming_message(
            header=header,
            sender_label=outcome.sender_anonymous_id,
            text=outcome.safe_text,
        )
        keyboard = message_actions_keyboard(
            message_id=outcome.message_id,
            conversation_id=outcome.conversation_id,
        )
        try:
            sent = await self._bot.send_message(
                chat_id=target_telegram_id,
                text=body,
                reply_markup=keyboard,
            )
        except Exception:  # noqa: BLE001 - delivery failures must not crash flow
            logger.warning(
                "Failed to deliver message %s to user %s",
                outcome.message_id,
                outcome.target_user_id,
            )
            return

        await self._messages.attach_telegram_message_id(
            outcome.message_id, sent.message_id
        )

    async def notify_seen(self, sender_telegram_id: int) -> None:
        """Tell the original sender that their message was seen (privacy-safe)."""
        try:
            await self._bot.send_message(
                chat_id=sender_telegram_id, text=fa.SEEN_NOTIFICATION
            )
        except Exception:  # noqa: BLE001
            logger.debug("Could not send seen notification to %s", sender_telegram_id)
