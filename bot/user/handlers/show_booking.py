from aiogram import Router
import logging
from aiogram.types import CallbackQuery
from bot.user.keyboards.cancellation_keyboard import (
    cancel_booking_button,
)
from db.db_reader import GetNotes
from utils.formatted_view import ViewController
from utils.message_templates import template_manager


logger = logging.getLogger(__name__)
show_booking_router = Router()


@show_booking_router.callback_query(lambda c: c.data == "all_notes")
async def show_all_notes(callback: CallbackQuery, user_id):

    notes = await GetNotes(user_id=user_id).get_notes()
    if notes:
        formatted_notes = ViewController(notes=notes, view_type="all").get()
        await callback.message.answer(text=formatted_notes, parse_mode="Markdown")
        await callback.answer()

    else:
        msg = template_manager.no_entries_found()
        await callback.message.answer(text=msg)
        await callback.answer()


@show_booking_router.callback_query(lambda c: c.data == "active_notes")
async def show_active_notes(callback: CallbackQuery, user_id):

    active_notes = await GetNotes(user_id=user_id, only_active=True).get_notes()
    cancel = cancel_booking_button(active_notes)
    logger.info(f"Active notes: {active_notes}")
    if active_notes:
        formatted_notes = ViewController(notes=active_notes, view_type="active").get()
        await callback.message.answer(
            text=f"{formatted_notes}", reply_markup=cancel, parse_mode="Markdown"
        )
        await callback.answer()
    else:
        msg = template_manager.no_entries_found()
        await callback.message.answer(text=msg)
        await callback.answer()
