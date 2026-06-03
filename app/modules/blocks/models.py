"""Block ORM model."""
from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, BigIntPk, TimestampMixin


class Block(Base, TimestampMixin):
    """A recipient blocking a given anonymous sender."""

    __tablename__ = "blocks"
    __table_args__ = (
        UniqueConstraint(
            "blocker_user_id", "blocked_anonymous_id", name="uq_block_pair"
        ),
    )

    id: Mapped[int] = mapped_column(BigIntPk, primary_key=True, autoincrement=True)
    blocker_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), index=True, nullable=False
    )
    blocked_anonymous_id: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )
