"""User ORM model."""
from __future__ import annotations

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, BigIntPk, TimestampMixin


class User(Base, TimestampMixin):
    """A bot user.

    - ``telegram_id`` is the real (private) Telegram id; never exposed to others.
    - ``anonymous_id`` is the label shown to recipients to correlate a sender.
    - ``public_token`` is embedded in the user's shareable deep link (rotatable).
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
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Lightweight per-user settings (e.g. seen notifications on/off).
    seen_notifications_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<User id={self.id} anon={self.anonymous_id}>"
