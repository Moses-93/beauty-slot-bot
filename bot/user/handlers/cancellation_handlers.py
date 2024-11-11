from aiogram import Router
from aiogram.types import CallbackQuery
from user_data import get_user_data
import logging
from utils.message_templates import template_manager
from utils.message_sender import manager
from db.db_writer import notes_manager

cancellation_router = Router()
logger = logging.getLogger(__name__)


@cancellation_router.callback_query(lambda c: c.data.startswith("note_"))
async def cancel_booking(callback: CallbackQuery, user_id):
    note_id = int(callback.data.split("_")[1])
    (note,) = get_user_data(user_id, "note")
    logger.info(f"Користувач з ID: {user_id} скасував запис на: {note}")
    msg_for_master = template_manager.message_to_the_master(
        username=note.username,
        service=note.service,
        date=note.free_date,
        time=note.time,
        booking_cancel=True,
    )
    await manager.send_message(user_id, message=msg_for_master)
    await notes_manager.delete(note_id=note_id)
    msg = template_manager.get_cancel_notification()
    await callback.message.answer(text=msg)
    await callback.answer()
