"""Centralized logging setup.

Note: message *content* is never logged; only ids and event names, to preserve
user privacy.
"""
from __future__ import annotations

import logging

_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


def setup_logging(level: str = "info") -> None:
    """Configure root logging once at startup."""
    logging.basicConfig(
        level=_LEVELS.get(level.lower(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger."""
    return logging.getLogger(name)
