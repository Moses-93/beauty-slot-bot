import ast
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
from decorators.check import check_user, deletion_checks
from utils.formatted_view import ViewController
from utils.message_sender import manager
from utils.message_templates import template_manager

date_router = Router()
logger = logging.getLogger(__name__)


@date_router.message(F.text == "Доступні дати")
@check_user.only_admin
async def show_dates(message: CallbackQuery, *args, **kwargs):
    free_dates = await GetFreeDate(free_dates=True).get()
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
@check_user.only_admin
async def delete_date(message: CallbackQuery, *args, **kwargs):
    msg = template_manager.get_select_service_or_date_del(date=True)
    delete = await free_dates_keyboard("delete")
    await message.answer(text=msg, reply_markup=delete)
    return


@date_router.message(F.text == "Назад")
@check_user.only_admin
async def back_to_main_menu(message: Message, *args, **kwargs):
    msg = "Ви повернулись на головне меню"
    keyboard = main_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
    return


@date_router.message(FreeDateForm.date)
@validator_date
async def set_date(message: Message, full_date, state: FSMContext, **kwargs):
    logger.info(f"FULL DATE: {full_date}")
    await date_manager.create(date=full_date.date(), free=True, now=full_date)
    await state.clear()
    msg = template_manager.get_add_new_date(date=full_date.date())
    await message.answer(text=msg)
    return


@date_router.callback_query(lambda c: c.data.startswith("delete_date_"))
@deletion_checks.prevent_deletion_if_related(date=True)
async def delete_selected_date(callback: CallbackQuery, *args, **kwargs):
    date_id = int(callback.data.split("_")[2])
    logger.info(f"date_id: {date_id} | TYPE: {type(date_id)}")
    await date_manager.delete(date_id)
    msg = template_manager.get_select_service_or_date_del(
        id=date_id, success=True, date=True
    )
    await callback.message.answer(text=msg)
    await callback.answer()


@date_router.callback_query(lambda c: c.data.startswith("del_date_"))
async def delete_booking(callback: CallbackQuery):
    _, _, date_id, user_ids = callback.data.split("_")
    user_ids = ast.literal_eval(user_ids)
    await date_manager.delete(date_id=int(date_id))
    msg_for_user = template_manager.get_delete_notification(date=True)
    for user_id in user_ids:
        logger.info(f"user_id: {user_id} | type: {type(user_id)}")
        await manager.send_message(chat_id=user_id, message=msg_for_user)
    msg = template_manager.get_select_service_or_date_del(active=True, date=True)
    await callback.message.answer(text=msg)
    await callback.answer()
