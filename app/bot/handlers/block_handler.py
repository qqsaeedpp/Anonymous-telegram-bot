"""Block flow with two-step confirmation.

block -> confirmation keyboard -> confirm/cancel. Blocking is performed by the
conversation's recipient against the (anonymous) sender label.
"""
from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.callbacks import BlockCancelCb, BlockCb, BlockConfirmCb, UnblockCb
from app.bot.keyboards.block_confirm import block_confirm_keyboard
from app.bot.keyboards.message_actions import seen_only_keyboard
from app.bot.texts import fa
from app.modules.blocks.service import BlockService
from app.modules.conversations.models import Conversation
from app.modules.conversations.service import ConversationService
from app.modules.users.models import User

router = Router(name="block")


async def _load_for_recipient(
    session: AsyncSession, conversation_id: int, user: User
) -> Conversation | None:
    """Return the conversation only if ``user`` is its recipient (anti-IDOR)."""
    conversation = await ConversationService(session).get_by_id(conversation_id)
    if conversation is None or conversation.recipient_user_id != user.id:
        return None
    return conversation


@router.callback_query(BlockCb.filter())
async def on_block_request(
    query: CallbackQuery,
    callback_data: BlockCb,
    session: AsyncSession,
    user: User,
) -> None:
    conversation = await _load_for_recipient(
        session, callback_data.conversation_id, user
    )
    if conversation is None:
        await query.answer(fa.CONVERSATION_NOT_FOUND, show_alert=True)
        return
    await query.message.answer(
        fa.BLOCK_CONFIRM_PROMPT,
        reply_markup=block_confirm_keyboard(conversation.id),
    )
    await query.answer()


@router.callback_query(BlockConfirmCb.filter())
async def on_block_confirm(
    query: CallbackQuery,
    callback_data: BlockConfirmCb,
    session: AsyncSession,
    user: User,
) -> None:
    conversation = await _load_for_recipient(
        session, callback_data.conversation_id, user
    )
    if conversation is None:
        await query.answer(fa.CONVERSATION_NOT_FOUND, show_alert=True)
        return
    await BlockService(session).block_from_conversation(conversation)
    try:
        await query.message.edit_text(fa.BLOCKED_DONE)
    except Exception:  # noqa: BLE001
        await query.message.answer(fa.BLOCKED_DONE)
    await query.answer()


@router.callback_query(BlockCancelCb.filter())
async def on_block_cancel(
    query: CallbackQuery,
    callback_data: BlockCancelCb,
    session: AsyncSession,
    user: User,
) -> None:
    try:
        await query.message.edit_text(fa.BLOCK_CANCELLED)
    except Exception:  # noqa: BLE001
        pass
    await query.answer()


@router.callback_query(UnblockCb.filter())
async def on_unblock(
    query: CallbackQuery,
    callback_data: UnblockCb,
    session: AsyncSession,
    user: User,
) -> None:
    conversation = await _load_for_recipient(
        session, callback_data.conversation_id, user
    )
    if conversation is None:
        await query.answer(fa.CONVERSATION_NOT_FOUND, show_alert=True)
        return
    await BlockService(session).unblock_from_conversation(conversation)
    try:
        await query.message.edit_reply_markup(
            reply_markup=seen_only_keyboard(conversation.id, blocked=False)
        )
    except Exception:  # noqa: BLE001
        pass
    await query.answer(fa.UNBLOCKED_DONE)
