"""Sanitization helpers for user-generated content.

All user text is HTML-escaped before being embedded into outgoing messages
(we send with parse_mode=HTML), and clamped to a maximum length.
"""
from __future__ import annotations

from html import escape


def sanitize_text(text: str, max_length: int) -> str:
    """Trim, length-clamp and HTML-escape user-provided text.

    Returns a string safe to embed inside an HTML-formatted Telegram message.
    """
    cleaned = text.strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return escape(cleaned)


def is_blank(text: str | None) -> bool:
    """Whether the given text is empty or whitespace-only."""
    return text is None or not text.strip()
