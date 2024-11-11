import ast
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from db.db_writer import service_manager
from bot.admin.states import ServiceForm, UpdateServiceForm
from datetime import timedelta
from db.db_reader import GetService
from ..keyboards.service_keybord import edit_service_keyboard
from bot.user.keyboards.booking_keyboard import services_keyboard
from bot.admin.keyboards.admin_keyboards import main_keyboard
from utils.formatted_view import ViewController
from utils.message_sender import manager
from utils.message_templates import template_manager
from decorators.check import check_user, deletion_checks
from decorators.validators.service_validator import (
    validate_service_name as val_srvc_name,
    validate_service_price as val_srvc_price,
    validate_service_durations as val_srvc_durations,
)

service_router = Router()
logger = logging.getLogger(__name__)


@service_router.message(F.text == "Показати послуги")
@check_user.only_admin
async def show_services(message: Message, *args, **kwargs):
    services = await GetService(all_services=True).get()
    if not services:
        await message.answer(text="Немає доступних послуг.")
        return
    formatted_services = ViewController(services=services).get()

    await message.answer(text=formatted_services, parse_mode="Markdown")
    return


@service_router.message(F.text == "Додати послугу")
@check_user.only_admin
async def add_service(message: Message, state: FSMContext, *args, **kwargs):
    msg = template_manager.get_add_new_service(name=True)
    logger.info(f"TYPE MSG: {type(msg)}")
    await message.answer(text=msg)
    await state.set_state(ServiceForm.name)
    return


@service_router.message(F.text == "Видалити послугу")
@check_user.only_admin
async def delete_service(message: Message, *args, **kwargs):
    delete = await services_keyboard("delete")
    msg = template_manager.get_select_service_del()
    await message.answer(text=msg, reply_markup=delete)
    return


@service_router.message(F.text == "Редагувати послугу")
@check_user.only_admin
async def choosing_service(message: Message, state: FSMContext, *args, **kwargs):
    await state.set_state("editing_service")
    edit = await services_keyboard("edit")
    msg = template_manager.get_edit_service()
    await message.answer(text=msg, reply_markup=edit)
    return


@service_router.message(F.text == "Назад")
@check_user.only_admin
async def back_to_main(message: Message, *args, **kwargs):
    msg = "Ви повернулися до головного меню"
    await message.answer(text=msg, reply_markup=main_keyboard)
    return


@service_router.message(ServiceForm.name)
@val_srvc_name
async def set_service_name(
    message: Message, service_name: str, state: FSMContext, **kwargs
):

    await state.update_data(name=service_name)
    msg = template_manager.get_add_new_service(price=True)
    await message.answer(text=msg)
    await state.set_state(ServiceForm.price)


@service_router.message(ServiceForm.price)
@val_srvc_price
async def set_service_price(message: Message, price, state: FSMContext, **kwargs):

    await state.update_data(price=price)
    msg = template_manager.get_add_new_service(durations=True)
    await message.answer(text=msg)
    await state.set_state(ServiceForm.durations)


@service_router.message(ServiceForm.durations)
@val_srvc_durations
async def set_service_duration(
    message: Message, durations: timedelta, state: FSMContext, **kwargs
):
    user_data = await state.get_data()
    name = user_data.get("name")
    price = user_data.get("price")
    await service_manager.create(name=name, price=price, durations=durations)
    await state.clear()
    msg = template_manager.get_add_new_service(success=True, service=name)
    await message.answer(text=msg)


@service_router.callback_query(lambda c: c.data.startswith("edit_service_"))
async def choosing_field(callback: CallbackQuery, state: FSMContext):
    logger.info(f"CALLBACK DATA(in choosing_field): {callback.data}")
    service_id = int(callback.data.split("_")[2])
    logger.info(f"service_id: {service_id}")

    await state.update_data(service_id=service_id)
    logger.info(f"service_id: {service_id}")
    msg = template_manager.get_edit_service(choice=True)
    await callback.message.answer(text=msg, reply_markup=edit_service_keyboard)
    await callback.answer()


@service_router.callback_query(lambda c: c.data.startswith("field_"))
async def set_field_value(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[1]
    logger.info(f"FIELD: {field}")
    await state.update_data(field=field)

    await state.set_state(UpdateServiceForm.field)
    msg = template_manager.get_edit_service(field=field)
    await callback.message.answer(text=msg)
    await callback.answer()


@service_router.message(UpdateServiceForm.field)
async def set_new_field_value(message: Message, state: FSMContext):
    new_value = message.text
    data = await state.get_data()
    field = data.get("field")
    service_id = data.get("service_id")
    new_value = (
        int(new_value) if field == "price" else timedelta(minutes=int(new_value))
    )
    logger.info(f"NEW_VALUE: {new_value} | TYPE: {type(new_value)}")
    logger.info(f"FIELD: {field}")
    logger.info(f"service_id: {service_id}")
    msg = template_manager.get_edit_service(field=field, new_value=new_value)
    await service_manager.update(service_id, **{field: new_value})
    logger.info(f"Поле {field} послуги з ID: {service_id} оновлено на {new_value}")
    await message.answer(text=msg)
    await state.clear()


@service_router.callback_query(lambda c: c.data.startswith("delete_service_"))
@deletion_checks.prevent_deletion_if_related(service=True)
async def delete_selected_service(callback: CallbackQuery, *args, **kwargs):
    service_id = int(callback.data.split("_")[2])
    await service_manager.delete(service_id)
    msg = template_manager.get_select_service_del(id=service_id, success=True)
    await callback.message.answer(text=msg)
    await callback.answer()


@service_router.callback_query(lambda c: c.data.startswith("del_service_"))
async def delete_booking(callback: CallbackQuery):
    logger.info(f"CALLBACK: {callback.data}")
    _, _, user_ids, service_id = callback.data.split("_")
    user_ids = ast.literal_eval(user_ids)
    await service_manager.delete(service_id=int(service_id))
    msg_fo_user = template_manager.get_delete_notification()
    for user_id in user_ids:
        await manager.send_message(chat_id=user_id, message=msg_fo_user)
        msg = template_manager.get_select_service_del(active=True)
        await callback.message.answer(text=msg)
    await callback.answer()
