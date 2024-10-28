from datetime import datetime, time
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.db_writer import date_manager
from ...keyboards.keyboards import free_dates_keyboard
from db.db_reader import GetFreeDate
from ..states import FreeDateForm
from aiogram.fsm.context import FSMContext
import logging
from decorators.validators.date_validator import validator_date

date_router = Router()
logger = logging.getLogger(__name__)


@date_router.callback_query(lambda c: c.data == "available_dates")
async def show_dates(callback: CallbackQuery):
    free_dates = GetFreeDate().get_all_free_dates()
    formatted_date = "\n".join([f"ID: {date.id}: {date.date}" for date in free_dates])
    await callback.message.answer(text=f"Доступні дати: \n\n{formatted_date}")
    await callback.answer()


@date_router.callback_query(lambda c: c.data == "add_date")
async def add_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FreeDateForm.date)
    await callback.message.answer(text="Введіть дату в форматі YYYY-MM-DD:")
    await callback.answer()


@date_router.message(FreeDateForm.date)
@validator_date
async def set_date(message: Message, full_date, state: FSMContext, **kwargs):
    await date_manager.create(date=full_date.date(), free=True, now=full_date)
    await state.clear()
    await message.answer(text=f"Дата - {full_date.date()} успішно додана!")


@date_router.callback_query(lambda c: c.data == "delete_date")
async def delete_date(callback: CallbackQuery):
    msg = "Виберіть дату, яку Ви хочете видалити:"
    delete = free_dates_keyboard("delete")
    await callback.message.answer(text=msg, reply_markup=delete)
    await callback.answer()


@date_router.callback_query(lambda c: c.data.startswith("delete_date_"))
async def delete_selected_date(callback: CallbackQuery):
    logger.info(f"CALLBACK DATA: {callback.data}")
    date_id = callback.data.split("_")[2]
    logger.info(f"date_id: {date_id}")
    date = await date_manager.delete(date_id)
    await callback.message.answer(text=f"Обрана Вами дата успішно видалена!")
    await callback.answer()
