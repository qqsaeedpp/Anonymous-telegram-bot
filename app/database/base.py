"""Declarative base and shared column mixins."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 64-bit integer everywhere, but mapped to SQLite's INTEGER so that
# autoincrement (rowid) works there. On PostgreSQL this stays BIGINT.
BigIntPk = BigInteger().with_variant(Integer, "sqlite")


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class TimestampMixin:
    """Adds created_at / updated_at columns (timezone-aware)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
