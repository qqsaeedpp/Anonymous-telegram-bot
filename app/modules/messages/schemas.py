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
