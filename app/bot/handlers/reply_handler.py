"""Reply flow: pressing the Reply button puts the user into REPLYING state.

The actual reply text is handled by message_handler based on this state.
"""
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.callbacks import ReplyCb
from app.bot.edit_utils import safe_edit
from app.bot.texts import fa
from app.modules.conversations.service import ConversationService
from app.modules.states.service import StateService
from app.modules.users.models import User

router = Router(name="reply")


@router.callback_query(ReplyCb.filter())
async def on_reply(
    query: CallbackQuery,
    callback_data: ReplyCb,
    session: AsyncSession,
    user: User,
) -> None:
    conversation = await ConversationService(session).get_by_id(
        callback_data.conversation_id
    )
    # Authorization: only participants may reply (anti-IDOR).
    if conversation is None or user.id not in (
        conversation.recipient_user_id,
        conversation.sender_user_id,
    ):
        await query.answer(fa.CONVERSATION_NOT_FOUND, show_alert=True)
        return

    await StateService(session).set_replying(user.id, conversation.id)
    # Edit in place: replace the revealed message with the reply prompt.
    await safe_edit(query, fa.REPLY_PROMPT)
    await query.answer()
