import ast
import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from datetime import timedelta

from ..keyboards.service_keybord import edit_service_keyboard
from ..middleware import AdminMiddleware

from src.db.crud import services_manager
from src.db.models import Service

from src.bot.admin.states import ServiceForm, UpdateServiceForm
from src.bot.user.keyboards.booking_keyboard import services_keyboard
from src.bot.admin.keyboards.general_keyboards import main_keyboard

from src.utils.message_sender import manager
from src.utils.message_templates import template_manager

from src.decorators.permissions import admin_only
from src.decorators.validation import (
    block_if_booked,
    validate_service_name as val_srvc_name,
    validate_service_price as val_srvc_price,
    validate_service_duration as val_srvc_durations,
)


logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(AdminMiddleware())
router.callback_query.middleware(AdminMiddleware())


@router.message(F.text == "Додати послугу")
@admin_only
async def add_service(message: Message, state: FSMContext, *args, **kwargs):
    msg = template_manager.get_add_new_service(name=True)
    logger.info(f"TYPE MSG: {type(msg)}")
    await message.answer(text=msg)
    await state.set_state(ServiceForm.name)
    return


@router.message(F.text == "Видалити послугу")
@admin_only
async def delete_service(message: Message, *args, **kwargs):
    services = await services_manager.read()
    if not services:
        msg = "Список послуг пустий"
        await message.answer(text=msg)
        return
    delete = await services_keyboard(act="delete", services=services)
    msg = template_manager.get_select_service_or_date_del()
    await message.answer(text=msg, reply_markup=delete)
    return


@router.message(F.text == "Редагувати послугу")
@admin_only
async def choosing_service(message: Message, state: FSMContext, *args, **kwargs):
    services = await services_manager.read()
    if not services:
        msg = template_manager.booking_not_found
        await message.answer(text=msg)
        return
    await state.set_state("editing_service")
    edit = await services_keyboard(act="edit", services=services)
    msg = template_manager.get_edit_service()
    await message.answer(text=msg, reply_markup=edit)
    return


@router.message(F.text == "Назад")
@admin_only
async def back_to_main(message: Message, state: FSMContext, *args, **kwargs):
    await state.clear()
    msg = "Ви повернулися до головного меню"
    await message.answer(text=msg, reply_markup=main_keyboard)
    return


@router.message(ServiceForm.name)
@val_srvc_name
async def set_service_name(
    message: Message, service_name: str, state: FSMContext, **kwargs
):

    await state.update_data(name=service_name)
    msg = template_manager.get_add_new_service(price=True)
    await message.answer(text=msg)
    await state.set_state(ServiceForm.price)


@router.message(ServiceForm.price)
@val_srvc_price
async def set_service_price(message: Message, price, state: FSMContext, **kwargs):

    await state.update_data(price=price)
    msg = template_manager.get_add_new_service(duration=True)
    await message.answer(text=msg)
    await state.set_state(ServiceForm.duration)


@router.message(ServiceForm.duration)
@val_srvc_durations
async def set_service_duration(
    message: Message, duration: timedelta, state: FSMContext, **kwargs
):
    user_data = await state.get_data()
    name = user_data.get("name")
    price = user_data.get("price")
    await services_manager.create(name=name, price=price, duration=duration)
    await state.clear()
    msg = template_manager.get_add_new_service(success=True, service=name)
    await message.answer(text=msg)


@router.callback_query(lambda c: c.data.startswith("edit_service_"))
async def choosing_field(callback: CallbackQuery, state: FSMContext):
    logger.info(f"CALLBACK DATA(in choosing_field): {callback.data}")
    service_id = int(callback.data.split("_")[2])
    await state.update_data(service_id=service_id)
    msg = template_manager.get_edit_service(choice=True)
    await callback.message.answer(text=msg, reply_markup=edit_service_keyboard)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("field_"))
async def set_field_value(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[1]
    logger.info(f"FIELD: {field}")
    await state.update_data(field=field)

    await state.set_state(UpdateServiceForm.field)
    msg = template_manager.get_edit_service(field=field)
    await callback.message.answer(text=msg)
    await callback.answer()


@router.message(UpdateServiceForm.field)
async def set_new_field_value(message: Message, state: FSMContext):
    new_value = message.text
    data = await state.get_data()
    field = data.get("field")
    service_id = data.get("service_id")
    if field == "price":
        new_value = int(new_value)
    elif field == "duration":
        new_value = timedelta(minutes=int(new_value))
    msg = template_manager.get_edit_service(field=field, new_value=new_value)
    await services_manager.update(Service.id == service_id, **{field: new_value})
    logger.info(f"Поле {field} послуги з ID: {service_id} оновлено на {new_value}")
    await message.answer(text=msg)
    await state.clear()
    return True


@router.callback_query(lambda c: c.data.startswith("delete_service_"))
@block_if_booked("service_id")
async def delete_selected_service(callback: CallbackQuery, service_id, *args, **kwargs):
    await services_manager.delete(id=service_id)
    msg = template_manager.get_select_service_or_date_del(id=service_id, success=True)
    await callback.message.answer(text=msg)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("del_service_id_"))
async def delete_booking(callback: CallbackQuery):
    logger.info(f"CALLBACK: {callback.data}")
    service_id = int(callback.data.split("_")[3])
    user_ids = ast.literal_eval(callback.data.split("_")[4])
    await services_manager.delete(id=service_id)
    msg_fo_user = template_manager.get_delete_notification()
    for user_id in user_ids:
        await manager.send_message(chat_id=user_id, message=msg_fo_user)
    msg = template_manager.get_select_service_or_date_del(active=True)
    await callback.message.answer(text=msg)
    await callback.answer()
