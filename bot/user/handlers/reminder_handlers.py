import logging
from aiogram import Router
from aiogram.types import CallbackQuery
from bot.user.keyboards.reminder_keyboard import create_reminder_keyboards
from db.db_writer import notes_manager
from user_data import get_user_data, user_data
from utils.message_templates import template_manager

logger = logging.getLogger(__name__)
reminder_router = Router()


@reminder_router.callback_query(lambda c: c.data.startswith("show_reminder_button"))
async def offers_reminders(callback: CallbackQuery, user_id):
    (note_id,) = get_user_data(user_id, "note_id")
    logger.info(f"NOTE ID -- {note_id}")
    logger.info(f"USER DATA -- {user_data}")
    msg = template_manager.get_reminder()
    keyboard = create_reminder_keyboards(note_id)
    await callback.message.answer(text=msg, reply_markup=keyboard)
    await callback.answer()


@reminder_router.callback_query(lambda c: c.data.startswith("reminder_"))
async def process_reminder_callback(callback: CallbackQuery, user_id):
    logger.info(f"hour(in procces reminder -- {callback.data})")
    _, hour, note_id = callback.data.split("_")
    logger.info(f"User selected time: {hour}, {note_id}")
    await notes_manager.update_reminder(note_id=int(note_id), reminder_hours=int(hour))
    msg = template_manager.get_reminder_notification(hour)
    await callback.message.answer(text=msg)
    await callback.answer()
    user_data.pop(user_id)
