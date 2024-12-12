import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from db.crud import notes_manager
from db.models import Notes

from utils.formatted_view import ViewController
from utils.message_templates import template_manager

from bot.user.keyboards.cancellation_keyboard import (
    cancel_booking_button,
)

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(lambda c: c.data == "all_notes")
async def show_all_notes(callback: CallbackQuery, user_id):
    logger.info(f"Користувач з ID: {user_id} переглядає всі записи")

    notes = await notes_manager.read(
        relations=(
            Notes.service,
            Notes.date,
        ),
        user_id=user_id,
    )
    if notes:
        formatted_notes = ViewController(notes=notes, view_type="all").get()
        await callback.message.answer(text=formatted_notes, parse_mode="Markdown")
        await callback.answer()
        return

    msg = template_manager.booking_not_found()
    await callback.message.answer(text=msg)
    await callback.answer()


@router.callback_query(lambda c: c.data == "active_notes")
async def show_active_notes(callback: CallbackQuery, user_id):
    logger.info(f"Користувач з ID: {user_id} переглядає активні записи")
    active_notes = await notes_manager.read(
        relations=(Notes.date, Notes.service),
        active=True,
        user_id=user_id,
    )
    if active_notes:
        cancel = await cancel_booking_button(active_notes)
        formatted_notes = ViewController(notes=active_notes, view_type="active").get()
        await callback.message.answer(
            text=f"{formatted_notes}", reply_markup=cancel, parse_mode="Markdown"
        )
        await callback.answer()
        return

    msg = template_manager.booking_not_found()
    await callback.message.answer(text=msg)
    await callback.answer()
