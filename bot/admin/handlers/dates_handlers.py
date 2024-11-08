from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.db_writer import date_manager
from bot.user.keyboards.booking_keyboard import free_dates_keyboard
from bot.admin.keyboards.admin_keyboards import main_keyboard
from db.db_reader import GetFreeDate
from ..states import FreeDateForm
from aiogram.fsm.context import FSMContext
import logging
from decorators.validators.date_validator import validator_date
from decorators.check_user import only_admin
from utils.formatted_view import ViewController

date_router = Router()
logger = logging.getLogger(__name__)


@date_router.message(F.text == "Доступні дати")
@only_admin
async def show_dates(message: CallbackQuery, *args, **kwargs):
    free_dates = await GetFreeDate(free_dates=True).get()
    if not free_dates:
        await message.answer(text="Немає доступних дат.")
        return
    formatted_date = ViewController(dates=free_dates).get()
    await message.answer(text=formatted_date, parse_mode="Markdown")
    return


@date_router.message(F.text == "Додати дату")
@only_admin
async def add_date(message: CallbackQuery, state: FSMContext, *args, **kwargs):
    await state.set_state(FreeDateForm.date)
    await message.answer(text="Введіть дату в форматі YYYY-MM-DD:")
    return


@date_router.message(FreeDateForm.date)
@validator_date
async def set_date(message: Message, full_date, state: FSMContext, **kwargs):
    logger.info(f"FULL DATE: {full_date}")
    await date_manager.create(date=full_date.date(), free=True, now=full_date)
    await state.clear()
    await message.answer(text=f"Дата - {full_date.date()} успішно додана!")
    return


@date_router.message(F.text == "Видалити дату")
@only_admin
async def delete_date(message: CallbackQuery, *args, **kwargs):
    msg = "Виберіть дату, яку Ви хочете видалити:"
    delete = await free_dates_keyboard("delete")
    await message.answer(text=msg, reply_markup=delete)
    return


@date_router.callback_query(lambda c: c.data.startswith("delete_date_"))
async def delete_selected_date(callback: CallbackQuery):
    logger.info(f"CALLBACK DATA(delete_selected_date): {callback.data}")
    date_id = int(callback.data.split("_")[2])
    logger.info(f"date_id: {date_id} | TYPE: {type(date_id)}")
    await date_manager.delete(date_id)
    await callback.message.answer(text=f"Обрана Вами дата успішно видалена!")
    await callback.answer()


@date_router.message(F.text == "Назад")
@only_admin
async def back_to_main_menu(message: Message, *args, **kwargs):
    msg = "Ви повернулись на головне меню"
    keyboard = main_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
    return
