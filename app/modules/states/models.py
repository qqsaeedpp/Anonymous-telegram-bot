"""Persistent user FSM state ORM model.

Stores the user's current interaction state so flows survive restarts. We keep
only ids in ``context_json`` (never sensitive content).
"""
from __future__ import annotations

import enum

from sqlalchemy import BigInteger, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class UserStateKind(str, enum.Enum):
    IDLE = "idle"
    # Waiting for the user to send the target @username (send-by-username flow).
    WAITING_FOR_TARGET_USERNAME = "waiting_for_target_username"
    # Waiting for the anonymous message text (target already resolved).
    WAITING_FOR_ANONYMOUS_MESSAGE = "waiting_for_anonymous_message"
    # Waiting for a reply text within a conversation.
    WAITING_FOR_REPLY = "waiting_for_reply"
    # Reserved: waiting for block confirmation (block uses inline buttons today).
    WAITING_FOR_BLOCK_CONFIRMATION = "waiting_for_block_confirmation"


class UserState(Base, TimestampMixin):
    __tablename__ = "user_states"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), primary_key=True
    )
    state: Mapped[UserStateKind] = mapped_column(
        Enum(UserStateKind, native_enum=False, length=40),
        default=UserStateKind.IDLE,
        nullable=False,
    )
    # JSON-encoded small context, e.g. {"recipient_user_id": 12} or
    # {"conversation_id": 7}. Stored as text for SQLite/PostgreSQL portability.
    context_json: Mapped[str | None] = mapped_column(Text, nullable=True)
