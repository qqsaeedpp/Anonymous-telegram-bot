"""Message business logic: send anonymous message, reply, mark seen.

This service contains no Telegram-API calls; it persists message records and
returns plain DTOs. Actual delivery to chats is performed by the bot layer via
the notifications service.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.blocks.service import BlockService
from app.modules.conversations.service import ConversationService
from app.modules.messages.models import (
    Message,
    MessageDirection,
    MessageStatus,
)
from app.modules.messages.repository import MessageRepository
from app.modules.messages.schemas import SendOutcome
from app.modules.users.models import User
from app.utils.text_sanitizer import sanitize_text


class MessageService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = MessageRepository(session)
        self._conversations = ConversationService(session)
        self._blocks = BlockService(session)

    async def send_anonymous(
        self, recipient: User, sender: User, raw_text: str, max_length: int
    ) -> SendOutcome:
        """Create the initial anonymous message from ``sender`` to ``recipient``."""
        safe_text = sanitize_text(raw_text, max_length)
        conversation = await self._conversations.get_or_create(recipient, sender)

        delivered = not await self._blocks.is_blocked(
            recipient.id, sender.anonymous_id
        )

        message = await self._repo.add(
            Message(
                conversation_id=conversation.id,
                direction=MessageDirection.TO_RECIPIENT,
                status=MessageStatus.SENT,
                text=safe_text,
            )
        )
        await self._conversations.touch(conversation)

        return SendOutcome(
            message_id=message.id,
            conversation_id=conversation.id,
            target_user_id=recipient.id,
            sender_anonymous_id=sender.anonymous_id,
            safe_text=safe_text,
            delivered=delivered,
        )

    async def send_reply(
        self, conversation, replier: User, raw_text: str, max_length: int
    ) -> SendOutcome:
        """Create a reply within an existing conversation.

        Direction and target are derived from who is replying. Replies stay in
        the same anonymous thread; neither side learns the other's identity.
        """
        safe_text = sanitize_text(raw_text, max_length)

        if replier.id == conversation.recipient_user_id:
            direction = MessageDirection.TO_SENDER
            target_user_id = conversation.sender_user_id
        else:
            direction = MessageDirection.TO_RECIPIENT
            target_user_id = conversation.recipient_user_id

        # Block check: the target must not have blocked this sender label.
        delivered = not await self._blocks.is_blocked(
            target_user_id, conversation.sender_anonymous_id
        )

        message = await self._repo.add(
            Message(
                conversation_id=conversation.id,
                direction=direction,
                status=MessageStatus.SENT,
                text=safe_text,
            )
        )
        await self._conversations.touch(conversation)

        return SendOutcome(
            message_id=message.id,
            conversation_id=conversation.id,
            target_user_id=target_user_id,
            sender_anonymous_id=conversation.sender_anonymous_id,
            safe_text=safe_text,
            delivered=delivered,
        )

    async def attach_telegram_message_id(
        self, message_id: int, telegram_message_id: int
    ) -> None:
        message = await self._repo.get_by_id(message_id)
        if message is not None:
            message.telegram_message_id = telegram_message_id
            message.status = MessageStatus.DELIVERED
            await self._session.flush()

    async def mark_seen(self, message_id: int, viewer: User) -> Message | None:
        """Mark a message as seen, enforcing that the viewer owns it.

        Returns the message if it was newly marked seen, else None.
        """
        message = await self._repo.get_by_id(message_id)
        if message is None:
            return None

        conversation = await self._conversations.get_by_id(message.conversation_id)
        if conversation is None:
            return None

        # Ownership/authorization check (prevents IDOR via crafted callback_data).
        is_owner = (
            message.direction == MessageDirection.TO_RECIPIENT
            and viewer.id == conversation.recipient_user_id
        ) or (
            message.direction == MessageDirection.TO_SENDER
            and viewer.id == conversation.sender_user_id
        )
        if not is_owner:
            return None

        if message.status == MessageStatus.SEEN:
            return None

        message.status = MessageStatus.SEEN
        message.seen_at = datetime.now(timezone.utc)
        await self._session.flush()
        return message
