"""Bot-specific configuration helpers (Bot/Dispatcher defaults)."""
from __future__ import annotations

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


def default_bot_properties() -> DefaultBotProperties:
    """Default formatting properties for outgoing messages.

    We default to HTML parse mode; all user-generated content MUST be escaped
    via app.utils.text_sanitizer before being embedded into a message.
    """
    return DefaultBotProperties(parse_mode=ParseMode.HTML)
