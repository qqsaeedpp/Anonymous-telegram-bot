"""Helpers to keep the chat tidy by editing the message a button lives on.

Callback handlers should reuse the message the user pressed instead of sending
a fresh one. ``safe_edit`` edits in place and silently tolerates the common
"message is not modified" / "message can't be edited" errors; if editing is not
possible at all (e.g. the message is too old), it falls back to sending a new
message so the user is never left without a response.
"""
from __future__ import annotations

from aiogram.types import CallbackQuery, InlineKeyboardMarkup


async def safe_edit(
    query: CallbackQuery,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    """Edit the callback's message in place, falling back to a new message."""
    message = query.message
    if message is None:  # message inaccessible/too old to edit
        return
    try:
        await message.edit_text(text, reply_markup=reply_markup)
    except Exception:  # noqa: BLE001 - unchanged content or non-editable message
        # Last resort so the user still gets feedback (rare edge cases only).
        try:
            await message.answer(text, reply_markup=reply_markup)
        except Exception:  # noqa: BLE001
            pass


__all__ = ["safe_edit"]
