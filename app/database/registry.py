"""Imports every ORM model so that ``Base.metadata`` is fully populated.

Import this module wherever the complete metadata is required (Alembic env,
create_all on startup). Importing models for their side effects only.
"""
from __future__ import annotations

from app.database.base import Base
from app.modules.blocks.models import Block
from app.modules.conversations.models import Conversation
from app.modules.messages.models import Message
from app.modules.states.models import UserState
from app.modules.users.models import User

__all__ = ["Base", "User", "Conversation", "Message", "Block", "UserState"]


async def create_all() -> None:
    """Create all tables (development convenience; use Alembic in production)."""
    from app.database.session import get_engine

    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
