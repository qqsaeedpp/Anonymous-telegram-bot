"""Cryptographically-secure token generation for public deep-link tokens.

Tokens are URL-safe and Telegram-compatible (A-Z a-z 0-9 _ -, <= 64 chars) and
carry a ``u_`` prefix so links read like ``?start=u_xxxxxxxx``. Always generated
with `secrets` (never `random`) and never derived from the user's telegram_id,
so they cannot be reverse-engineered.
"""
from __future__ import annotations

import secrets

_PREFIX = "u_"
# Telegram allows up to 64 chars in the start parameter; we stay well below.
_DEFAULT_NBYTES = 9  # ~12 url-safe characters


def generate_public_token(nbytes: int = _DEFAULT_NBYTES) -> str:
    """Return a random URL-safe public token, prefixed with ``u_``."""
    return _PREFIX + secrets.token_urlsafe(nbytes)
