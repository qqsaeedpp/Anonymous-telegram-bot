"""User ORM model."""
from __future__ import annotations

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, BigIntPk, TimestampMixin


class User(Base, TimestampMixin):
    """A bot user.

    - ``telegram_id`` is the real (private) Telegram id; only ever used
      internally — never exposed to other users.
    - ``anonymous_id`` is the numeric label shown to recipients to correlate a
      sender. Random, never derived from telegram_id.
    - ``public_token`` is embedded in the user's shareable deep link (rotatable).
    - ``username_snapshot`` is a copy of the user's Telegram @username, used ONLY
      to find members via the "send message" button. Never shown in anonymous
      messages.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigIntPk, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    anonymous_id: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )
    public_token: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )

    # Snapshots of the Telegram profile (kept fresh on each /start).
    # username_snapshot is indexed because it is the lookup key for the
    # username-based send flow. It is NOT exposed in any anonymous message.
    username_snapshot: Mapped[str | None] = mapped_column(
        String(64), index=True, nullable=True
    )
    first_name_snapshot: Mapped[str | None] = mapped_column(String(128), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Lightweight per-user settings (e.g. seen notifications on/off).
    seen_notifications_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<User id={self.id} anon={self.anonymous_id}>"
