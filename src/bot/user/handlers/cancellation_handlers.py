import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from utils.message_templates import template_manager
from utils.message_sender import manager

from db.crud import notes_manager


logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data.startswith("note_"))
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
    await notes_manager.delete(id=int(note_id))
    msg = template_manager.get_cancel_notification()
    await callback.message.answer(text=msg)
    await callback.answer()
