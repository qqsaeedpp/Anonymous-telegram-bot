"""Database configuration helpers."""
from __future__ import annotations

from app.config.settings import get_settings


def get_database_url() -> str:
    """Return the configured SQLAlchemy async database URL."""
    return get_settings().database_url


def is_sqlite(url: str | None = None) -> bool:
    """Whether the configured database is SQLite (affects connect args)."""
    return (url or get_database_url()).startswith("sqlite")
