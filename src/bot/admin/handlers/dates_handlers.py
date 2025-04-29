import ast
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime

from ..states import FreeDateForm
from ..middleware import AdminMiddleware

from db.crud import dates_manager

from bot.user.keyboards.booking_keyboard import free_dates_keyboard
from bot.admin.keyboards.general_keyboards import main_keyboard


from decorators.validation import validate_date, block_if_booked
from decorators.permissions import admin_only

from utils.message_sender import manager
from utils.message_templates import template_manager


logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(AdminMiddleware())


@router.message(F.text == "Додати дату")
@admin_only
async def add_date(message: CallbackQuery, state: FSMContext, *args, **kwargs):
    await state.set_state(FreeDateForm.date)
    msg = template_manager.get_add_new_date(add=True)
    await message.answer(text=msg)
    return


@router.message(F.text == "Видалити дату")
@admin_only
async def delete_date(message: CallbackQuery, *args, **kwargs):
    now = datetime.now()
    dates = await dates_manager.read(free=True)
    msg = template_manager.get_select_service_or_date_del(date=True)
    delete = await free_dates_keyboard(act="delete", free_dates=dates)
    await message.answer(text=msg, reply_markup=delete)
    return


@router.message(F.text == "Назад")
@admin_only
async def back_to_main_menu(message: Message, state: FSMContext, *args, **kwargs):
    await state.clear()
    msg = "Ви повернулись на головне меню"
    keyboard = main_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
    return


@router.message(FreeDateForm.date)
@validate_date
async def set_date(message: Message, full_date, state: FSMContext, **kwargs):
    logger.info(f"FULL DATE: {full_date}")
    await dates_manager.create(date=full_date.date(), del_time=full_date)
    await state.clear()
    msg = template_manager.get_add_new_date(date=full_date.date())
    await message.answer(text=msg)
    return


@router.callback_query(lambda c: c.data.startswith("delete_date_"))
@block_if_booked("date_id")
async def delete_selected_date(callback: CallbackQuery, date_id: int, *args, **kwargs):
    logger.info(f"date_id: {date_id} | TYPE: {type(date_id)}")
    await dates_manager.delete(id=date_id)
    msg = template_manager.get_select_service_or_date_del(
        id=date_id, success=True, date=True
    )
    await callback.message.answer(text=msg)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("del_date_id_"))
async def delete_booking(callback: CallbackQuery):
    date_id = int(callback.data.split("_")[3])
    user_ids = ast.literal_eval(callback.data.split("_")[4])
    msg_for_user = template_manager.get_delete_notification(date=True)
    for user_id in user_ids:
        logger.info(f"Message sender: {user_id}")
        await manager.send_message(chat_id=user_id, message=msg_for_user)
    await dates_manager.delete(date_id=date_id)
    msg = template_manager.get_select_service_or_date_del(active=True, date=True)
    await callback.message.answer(text=msg)
    await callback.answer()
