from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from db.db_writer import service_manager
from bot.admin.states import ServiceForm, UpdateServiceForm
from datetime import timedelta
from db.db_reader import GetService
from ..keyboards.service_keybord import edit_service_keyboard
from ...keyboards.keyboards import services_keyboard
import logging
from utils.formatted_view import format_services
from decorators.validators.service_validator import (
    validate_service_name as val_srvc_name,
    validate_service_price as val_srvc_price,
    validate_service_durations as val_srvc_durations,
)

service_router = Router()
logger = logging.getLogger(__name__)


@service_router.callback_query(lambda c: c.data.startswith("show_services"))
async def show_services(callback: CallbackQuery, *args, **kwargs):
    services = await GetService().get_all_services()
    formatted_services = format_services(services)

    await callback.message.answer(
        text=formatted_services, parse_mode="Markdown"
    )
    await callback.answer()


@service_router.callback_query(lambda c: c.data.startswith("add_service"))
async def add_service(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Для того, щоб додати послугу - заповніть всі запропоновані поля.\nВведіть назву послуги:"
    )
    await state.set_state(ServiceForm.name)
    await callback.answer()


@service_router.message(ServiceForm.name)
@val_srvc_name
async def set_service_name(
    message: Message, service_name: str, state: FSMContext, **kwargs
):

    await state.update_data(name=service_name)

    await message.answer(text="Вкажіть ціну послуги:")
    await state.set_state(ServiceForm.price)


@service_router.message(ServiceForm.price)
@val_srvc_price
async def set_service_price(message: Message, price, state: FSMContext, **kwargs):

    await state.update_data(price=price)
    await message.answer(text="Вкажіть тривалість послуги у хвилинах: ")
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
    await message.answer(text=f"Послуга - {name} успішно додана!")


@service_router.callback_query(lambda c: c.data == "edit_services")
async def choosing_service(callback: CallbackQuery, state: FSMContext):
    logger.info(f"CALLBACK DATA: {callback.data}")
    await state.set_state("editing_service")
    edit = await services_keyboard("edit")
    await callback.message.answer(
        text="Оберіть, яку послугу Ви хочете редагувати", reply_markup=edit
    )
    await callback.answer()


@service_router.callback_query(lambda c: c.data.startswith("edit_service_"))
async def choosing_field(callback: CallbackQuery, state: FSMContext):
    logger.info(f"CALLBACK DATA(in choosing_field): {callback.data}")
    service_id = int(callback.data.split("_")[2])
    logger.info(f"service_id: {service_id}")

    await state.update_data(service_id=service_id)
    logger.info(f"service_id: {service_id}")
    await callback.message.answer(
        text="Оберіть, яке поле Ви хочете редагувати",
        reply_markup=edit_service_keyboard,
    )
    await callback.answer()


@service_router.callback_query(lambda c: c.data.startswith("field_"))
async def set_field_value(callback: CallbackQuery, state: FSMContext):
    field = callback.data.split("_")[1]
    logger.info(f"FIELD: {field}")
    await state.update_data(field=field)

    await state.set_state(UpdateServiceForm.field)
    if field == "durations":
        await callback.message.answer(
            f"Введіть нове значення поля {field} в хвилинах: "
        )
        await callback.answer()
    else:
        await callback.message.answer(f"Введіть нове значення поля {field}: ")
        await callback.answer()


@service_router.message(UpdateServiceForm.field)
async def set_new_field_value(message: Message, state: FSMContext):
    new_value = message.text
    data = await state.get_data()
    field = data.get("field")
    service_id = data.get("service_id")
    if field == "durations":
        new_value = timedelta(minutes=int(new_value))
    logger.info(f"NEW_VALUE: {new_value}")
    logger.info(f"FIELD: {field}")
    logger.info(f"service_id: {service_id}")

    await service_manager.update(service_id, **{field: new_value})
    await message.answer(f"Значення поля {field} успішно змінено на {new_value}!")
    await state.clear()


@service_router.callback_query(lambda c: c.data == "delete_service")
async def delete_service(callback: CallbackQuery):
    logger.info(f"CALLBACK DATA: {callback.data}")
    delete = await services_keyboard("delete")
    await callback.message.answer(
        text="Оберіть, яку послугу Ви хочете видалити", reply_markup=delete
    )
    await callback.answer()


@service_router.callback_query(lambda c: c.data.startswith("delete_service_"))
async def delete_selected_service(callback: CallbackQuery):
    service_id = int(callback.data.split("_")[2])
    await service_manager.delete(service_id)
    await callback.message.answer(text="Послуга успішно видалена!")
    await callback.answer()
