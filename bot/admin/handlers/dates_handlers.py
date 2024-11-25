import ast
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.db_writer import date_manager
from bot.user.keyboards.booking_keyboard import free_dates_keyboard
from bot.admin.keyboards.admin_keyboards import main_keyboard
from decorators.caching.request_cache import clear_cache, get_free_dates, update_cache
from ..states import FreeDateForm
from aiogram.fsm.context import FSMContext
import logging
from decorators.validators.date_validator import validator_date
from decorators.check import check_user, deletion_checks
from utils.formatted_view import ViewController
from utils.message_sender import manager
from utils.message_templates import template_manager
from cache.cache import request_cache


date_router = Router()
logger = logging.getLogger(__name__)


@date_router.message(F.text == "Доступні дати")
@get_free_dates
@check_user.only_admin
async def show_dates(message: CallbackQuery, free_dates, *args, **kwargs):
    if not free_dates:
        await message.answer(text="Немає доступних дат.")
        return
    formatted_date = ViewController(dates=free_dates).get()
    await message.answer(text=formatted_date, parse_mode="Markdown")
    return


@date_router.message(F.text == "Додати дату")
@check_user.only_admin
async def add_date(message: CallbackQuery, state: FSMContext, *args, **kwargs):
    await state.set_state(FreeDateForm.date)
    msg = template_manager.get_add_new_date(add=True)
    await message.answer(text=msg)
    return


@date_router.message(F.text == "Видалити дату")
@get_free_dates
@check_user.only_admin
async def delete_date(message: CallbackQuery, dates, *args, **kwargs):
    msg = template_manager.get_select_service_or_date_del(date=True)
    delete = await free_dates_keyboard(act="delete", free_dates=dates)
    await message.answer(text=msg, reply_markup=delete)
    return


@date_router.message(F.text == "Назад")
@check_user.only_admin
async def back_to_main_menu(message: Message, state: FSMContext, *args, **kwargs):
    await state.clear()
    msg = "Ви повернулись на головне меню"
    keyboard = main_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
    return


@date_router.message(FreeDateForm.date)
@update_cache(key="dates")
@validator_date
async def set_date(message: Message, full_date, state: FSMContext, **kwargs):
    logger.info(f"FULL DATE: {full_date}")
    await date_manager.create(date=full_date.date(), del_time=full_date)
    await state.clear()
    msg = template_manager.get_add_new_date(date=full_date.date())
    await message.answer(text=msg)
    return


@date_router.callback_query(lambda c: c.data.startswith("delete_date_"))
@clear_cache(key="dates")
@deletion_checks.check_booking("date_id")
async def delete_selected_date(callback: CallbackQuery, date_id: int, *args, **kwargs):
    logger.info(f"date_id: {date_id} | TYPE: {type(date_id)}")
    await date_manager.delete(date_id)
    msg = template_manager.get_select_service_or_date_del(
        id=date_id, success=True, date=True
    )
    await callback.message.answer(text=msg)
    await callback.answer()


@date_router.callback_query(lambda c: c.data.startswith("del_date_id_"))
@clear_cache(key="dates")
async def delete_booking(callback: CallbackQuery, *args, **kwargs):
    date_id = int(callback.data.split("_")[3])
    user_ids = await request_cache.get_request("user_ids")
    msg_for_user = template_manager.get_delete_notification(date=True)
    for user_id in user_ids:
        logger.info(f"User_id: {user_id}")
        await manager.send_message(chat_id=user_id, message=msg_for_user)
    await date_manager.delete(date_id=int(date_id))
    msg = template_manager.get_select_service_or_date_del(active=True, date=True)
    await callback.message.answer(text=msg)
    await callback.answer()
