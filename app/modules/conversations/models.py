"""Conversation ORM model.

A conversation is a two-way anonymous thread between a sender and a recipient.
Neither side ever learns the other's real Telegram identity.
"""
from __future__ import annotations

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, BigIntPk, TimestampMixin


class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"
    __table_args__ = (
        UniqueConstraint(
            "recipient_user_id", "sender_user_id", name="uq_conversation_pair"
        ),
    )

    id: Mapped[int] = mapped_column(BigIntPk, primary_key=True, autoincrement=True)

    recipient_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), index=True, nullable=False
    )
    sender_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), index=True, nullable=False
    )

    # The label the recipient sees for this sender (snapshot of sender.anonymous_id).
    sender_anonymous_id: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )

    # Fast snapshot of whether the recipient has blocked this sender.
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    last_message_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
