"""Session factory and unit-of-work helpers.

A single engine and sessionmaker are created at startup via ``init_engine``.
Handlers obtain a session per-update through the middleware, which wraps the
work in a transaction (commit on success, rollback on error).
"""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.database.connection import create_engine

_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def init_engine(echo: bool = False) -> AsyncEngine:
    """Initialize the global engine and sessionmaker (idempotent)."""
    global _engine, _sessionmaker
    if _engine is None:
        _engine = create_engine(echo=echo)
        _sessionmaker = async_sessionmaker(
            _engine, expire_on_commit=False, autoflush=False
        )
    return _engine


def get_engine() -> AsyncEngine:
    if _engine is None:
        raise RuntimeError("Engine not initialized. Call init_engine() first.")
    return _engine


async def dispose_engine() -> None:
    """Dispose the engine on shutdown."""
    global _engine, _sessionmaker
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _sessionmaker = None


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Provide a transactional session scope.

    Commits on success, rolls back on exception, always closes.
    """
    if _sessionmaker is None:
        raise RuntimeError("Sessionmaker not initialized. Call init_engine() first.")
    session = _sessionmaker()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
