import logging

from aiogram import Router
from aiogram.types import CallbackQuery

from ..keyboards.reminder_keyboard import create_reminder_keyboards

from src.db.models import Booking
from src.db.crud import notes_manager

from src.cache.cache import user_cache

from src.utils.message_templates import template_manager


logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data.startswith("show_reminder_button"))
async def offers_reminders(callback: CallbackQuery, user_id):
    logger.info("Запуск обробника пропозиції нагадувань")
    (note_id,) = await user_cache.get_user_cache(user_id, "note_id")
    logger.info(f"note_id: {note_id}")
    msg = template_manager.get_reminder(choice=True)
    keyboard = create_reminder_keyboards(note_id)
    await callback.message.answer(text=msg, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("reminder_"))
async def process_reminder_callback(callback: CallbackQuery, user_id):
    logger.info(f"Запуск обробника нагадування")
    _, hour, note_id = callback.data.split("_")
    logger.info(f"hour: {hour} | note_id: {note_id}")
    await notes_manager.update(Booking.id == int(note_id), reminder_hours=int(hour))
    msg = template_manager.get_reminder(hour=hour)
    await callback.message.answer(text=msg)
    await callback.answer()
    await user_cache.clear_user_cache(user_id)
