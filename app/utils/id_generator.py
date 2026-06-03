"""Anonymous id generation.

``anonymous_id`` is the (numeric) label a recipient sees so they can correlate
multiple messages from the same — still anonymous — sender. It is a random
number, never derived from telegram_id, so it cannot be reverse-engineered.
Stored as a string for portability, but it is purely numeric (e.g. ``"546372"``).
"""
from __future__ import annotations

import secrets

# 6-digit number range [100000, 999999]. Collisions are resolved by retrying
# against the DB (see app.modules.links.token_service), so this stays readable.
_MIN = 100_000
_SPAN = 900_000


def generate_anonymous_id() -> str:
    """Return a random numeric anonymous id as a string (e.g. ``"546372"``)."""
    return str(_MIN + secrets.randbelow(_SPAN))
