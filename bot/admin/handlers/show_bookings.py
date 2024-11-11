from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from db.db_reader import GetNotes
from utils.formatted_view import ViewController
from ..keyboards.show_booking_keyboards import show_periods
from ..keyboards.admin_keyboards import main_keyboard
from decorators.check.check_user import only_admin
from utils.message_templates import template_manager

show_booking_router = Router()


@show_booking_router.message(F.text == "Фільтрувати записи")
@only_admin
async def filtered_bookings(message: Message, *args, **kwargs):
    msg = "Оберіть за скільки днів ви хочете переглянути записи"
    await message.answer(text=msg, reply_markup=show_periods)


@show_booking_router.message(F.text == "Всі активні записи")
@only_admin
async def show_active_notes(message: Message, *args, **kwargs):
    active_notes = await GetNotes(only_active=True).get_notes()
    if not active_notes:
        msg = template_manager.booking_not_found()
        await message.answer(text=msg)
        return
    formatted_notes = ViewController(notes=active_notes, view_type="master").get()
    await message.answer(text=formatted_notes, parse_mode="Markdown")


@show_booking_router.callback_query(lambda c: c.data.startswith("days_"))
async def show_bookings_for_1_day(callback: CallbackQuery):
    date = int(callback.data.split("_")[1])
    all_notes = await GetNotes(day_filter=date).get_notes()
    if not all_notes:
        msg = template_manager.booking_not_found()
        await callback.message.answer(text=msg)
        return
    formatted_notes = ViewController(notes=all_notes, view_type="master").get()
    await callback.message.answer(text=formatted_notes, parse_mode="Markdown")
    await callback.answer()


@show_booking_router.message(F.text == "Назад")
@only_admin
async def back_to_general(message: Message, *args, **kwargs):
    msg = "Ви повернулись до головного меню"
    await message.answer(text=msg, reply_markup=main_keyboard)
