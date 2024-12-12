import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from datetime import datetime, timedelta

from ..keyboards.show_booking_keyboards import show_periods
from ..keyboards.general_keyboards import main_keyboard
from ..middleware import AdminMiddleware

from db.crud import notes_manager
from db.models import Dates, Notes

from decorators.permissions import admin_only

from utils.message_templates import template_manager
from utils.formatted_view import ViewController

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(AdminMiddleware())
router.message.middleware(AdminMiddleware())


@router.message(F.text == "Фільтрувати записи")
@admin_only
async def filtered_bookings(message: Message, *args, **kwargs):
    msg = "Оберіть за скільки днів ви хочете переглянути записи"
    await message.answer(text=msg, reply_markup=show_periods)
    return


@router.message(F.text == "Всі активні записи")
@admin_only
async def show_active_notes(message: Message, *args, **kwargs):
    logger.info(f"Запуск обробника для показу всіх активних записів")
    active_notes = await notes_manager.read(active=True)
    if not active_notes:
        msg = template_manager.booking_not_found()
        await message.answer(text=msg)
        return
    logger.info(f"Active: {active_notes}")
    formatted_notes = ViewController(notes=active_notes, view_type="master").get()
    await message.answer(text=formatted_notes, parse_mode="Markdown")


@router.message(F.text == "Назад")
@admin_only
async def back_to_general(message: Message, *args, **kwargs):
    msg = "Ви повернулись до головного меню"
    await message.answer(text=msg, reply_markup=main_keyboard)


@router.callback_query(lambda c: c.data.startswith("days_"))
async def show_bookings_by_days(callback: CallbackQuery):
    day = int(callback.data.split("_")[1])
    date = datetime.now() - timedelta(days=day)
    notes = await notes_manager.read(expressions=(Notes.date.has(Dates.date >= date),))
    if not notes:
        msg = template_manager.booking_not_found()
        await callback.message.answer(text=msg)
        return
    formatted_notes = ViewController(notes=notes, view_type="master").get()
    await callback.message.answer(text=formatted_notes, parse_mode="Markdown")
    await callback.answer()
