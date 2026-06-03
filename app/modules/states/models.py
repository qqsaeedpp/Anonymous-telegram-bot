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
    COMPOSING = "composing"  # writing an anonymous message to a recipient
    REPLYING = "replying"  # replying within a conversation


class UserState(Base, TimestampMixin):
    __tablename__ = "user_states"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), primary_key=True
    )
    state: Mapped[UserStateKind] = mapped_column(
        Enum(UserStateKind, native_enum=False, length=20),
        default=UserStateKind.IDLE,
        nullable=False,
    )
    # JSON-encoded small context, e.g. {"recipient_user_id": 12} or
    # {"conversation_id": 7}. Stored as text for SQLite/PostgreSQL portability.
    context_json: Mapped[str | None] = mapped_column(Text, nullable=True)
