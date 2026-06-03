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
from app.modules.messages.schemas import SendOutcome, ViewResult
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
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
            is_reply=False,
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

        # The target sees the *author's* anonymous label (i.e. the replier's).
        author_label = replier.anonymous_id

        # Block check: the target must not have blocked the author's label.
        delivered = not await self._blocks.is_blocked(target_user_id, author_label)

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
            sender_anonymous_id=author_label,
            safe_text=safe_text,
            delivered=delivered,
            is_reply=True,
        )

    async def attach_telegram_message_id(
        self, message_id: int, telegram_message_id: int
    ) -> None:
        message = await self._repo.get_by_id(message_id)
        if message is not None:
            message.telegram_message_id = telegram_message_id
            message.status = MessageStatus.DELIVERED
            await self._session.flush()

    async def view(self, message_id: int, viewer: User) -> ViewResult | None:
        """Reveal a message to its rightful owner, marking it seen (once).

        Enforces ownership (anti-IDOR). The text is returned every time the
        owner opens it, but the "seen" notification is flagged for sending only
        the first time. Returns ``None`` if the viewer is not authorized.
        """
        message = await self._repo.get_by_id(message_id)
        if message is None:
            return None

        conversation = await self._conversations.get_by_id(message.conversation_id)
        if conversation is None:
            return None

        is_to_recipient = message.direction == MessageDirection.TO_RECIPIENT
        if is_to_recipient:
            if viewer.id != conversation.recipient_user_id:
                return None
            author_id = conversation.sender_user_id
        else:
            if viewer.id != conversation.sender_user_id:
                return None
            author_id = conversation.recipient_user_id

        author = await UserRepository(self._session).get_by_id(author_id)
        author_label = (
            author.anonymous_id if author else conversation.sender_anonymous_id
        )

        if message.status != MessageStatus.SEEN:
            message.status = MessageStatus.SEEN
            message.seen_at = datetime.now(timezone.utc)

        should_notify_seen = not message.seen_notification_sent
        if should_notify_seen:
            message.seen_notification_sent = True

        await self._session.flush()

        viewer_is_recipient = viewer.id == conversation.recipient_user_id
        is_blocked = False
        if viewer_is_recipient:
            is_blocked = await self._blocks.is_blocked(
                viewer.id, conversation.sender_anonymous_id
            )

        return ViewResult(
            message_id=message.id,
            conversation_id=conversation.id,
            safe_text=message.text or "",
            author_label=author_label,
            author_user_id=author_id,
            is_reply=not is_to_recipient,
            should_notify_seen=should_notify_seen,
            viewer_is_recipient=viewer_is_recipient,
            is_blocked=is_blocked,
        )
