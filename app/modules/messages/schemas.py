"""Data-transfer objects for message flows (no ORM / Telegram leakage)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SendOutcome:
    """Result of attempting to send an anonymous message or reply.

    - ``delivered`` is False when the target has blocked the sender. The caller
      should still show a neutral "sent" message to avoid leaking block status.
    """

    message_id: int
    conversation_id: int
    target_user_id: int
    sender_anonymous_id: str
    safe_text: str
    delivered: bool
    is_reply: bool = False


@dataclass(frozen=True)
class ViewResult:
    """Result of a recipient opening ("viewing") an anonymous message."""

    message_id: int
    conversation_id: int
    safe_text: str
    # The anonymous label the viewer sees for the message's author.
    author_label: str
    author_user_id: int
    is_reply: bool
    # True only the first time the message is seen -> notify the author once.
    should_notify_seen: bool
    # Whether the viewer is the conversation recipient (only they may block).
    viewer_is_recipient: bool
    # Whether the viewer has already blocked this sender (block vs unblock button).
    is_blocked: bool
