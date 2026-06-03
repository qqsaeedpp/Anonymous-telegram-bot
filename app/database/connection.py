"""Async engine creation."""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config.database_config import get_database_url, is_sqlite


def create_engine(echo: bool = False) -> AsyncEngine:
    """Create the async SQLAlchemy engine for the configured database."""
    url = get_database_url()
    connect_args: dict = {}
    if is_sqlite(url):
        # Allow usage across the asyncio event loop's threads.
        connect_args = {"check_same_thread": False}
    return create_async_engine(url, echo=echo, future=True, connect_args=connect_args)
