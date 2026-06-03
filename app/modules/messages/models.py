"""Message ORM model and enums."""
from __future__ import annotations

import enum

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, BigIntPk, TimestampMixin


class MessageDirection(str, enum.Enum):
    """Who the message is delivered to within a conversation."""

    TO_RECIPIENT = "to_recipient"  # the original anonymous message
    TO_SENDER = "to_sender"  # a reply back to the original sender


class MessageStatus(str, enum.Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    SEEN = "seen"


class ContentType(str, enum.Enum):
    TEXT = "text"
    # Future: PHOTO, VIDEO, FILE ...


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigIntPk, primary_key=True, autoincrement=True)

    conversation_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("conversations.id"), index=True, nullable=False
    )

    direction: Mapped[MessageDirection] = mapped_column(
        Enum(MessageDirection, native_enum=False, length=20), nullable=False
    )
    content_type: Mapped[ContentType] = mapped_column(
        Enum(ContentType, native_enum=False, length=20),
        default=ContentType.TEXT,
        nullable=False,
    )
    status: Mapped[MessageStatus] = mapped_column(
        Enum(MessageStatus, native_enum=False, length=20),
        default=MessageStatus.SENT,
        nullable=False,
    )

    text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # The Telegram message id of the delivered copy (for seen tracking / edits).
    telegram_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    seen_at: Mapped[object | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
