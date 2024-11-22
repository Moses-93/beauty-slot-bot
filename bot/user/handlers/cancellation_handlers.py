from aiogram import Router
from aiogram.types import CallbackQuery
import logging
from utils.message_templates import template_manager
from utils.message_sender import manager
from db.db_writer import notes_manager

cancellation_router = Router()
logger = logging.getLogger(__name__)


@cancellation_router.callback_query(lambda c: c.data.startswith("note_"))
async def cancel_booking(callback: CallbackQuery, user_id):
    _, note_id, name, date, time = callback.data.split("_")
    msg_for_master = await template_manager.message_to_the_master(
        username=name,
        date=date,
        service=None,
        time=time,
        booking_cancel=True,
    )
    await manager.send_message(user_id, message=msg_for_master)
    await notes_manager.delete(note_id=int(note_id))
    msg = template_manager.get_cancel_notification()
    await callback.message.answer(text=msg)
    await callback.answer()
