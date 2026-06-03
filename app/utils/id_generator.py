"""Anonymous id generation.

`anonymous_id` is the label a recipient sees so they can correlate multiple
messages from the same (still anonymous) sender. It is random, never derived
from telegram_id, and prefixed for readability in the UI.
"""
from __future__ import annotations

import secrets

_PREFIX = "anon-"
_DEFAULT_NBYTES = 6  # ~8 url-safe characters


def generate_anonymous_id(nbytes: int = _DEFAULT_NBYTES) -> str:
    """Return a random, human-readable anonymous id (e.g. ``anon-7Kp3Qz``)."""
    return _PREFIX + secrets.token_urlsafe(nbytes)
