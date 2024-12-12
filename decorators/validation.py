import re
import logging

from aiogram.types import Message, CallbackQuery

from datetime import datetime, timedelta, time

from bot.admin.keyboards.general_keyboards import delete_booking_keyboard

from db.crud import services_manager, dates_manager, notes_manager

from cache.cache import user_cache

from utils.message_templates import template_manager

logger = logging.getLogger(__name__)


def require_field(fields: list):
    def decorator(func):
        async def wrapper(event: CallbackQuery | Message, *args, **kwargs):
            user_id = event.from_user.id

            async def send_message(text: str):
                if isinstance(event, Message):
                    await event.answer(text=text)
                    return

                elif isinstance(event, CallbackQuery):
                    await event.message.answer(text=text)
                    await event.answer()
                    return

            user_data = await user_cache.get_user_cache(user_id=user_id)

            if not user_data or not all(field in user_data for field in fields):
                await send_message(text="Спочатку оберіть послугу й дату")
                return

            return await func(event, *args, **kwargs)

        return wrapper

    return decorator


def validate_service_name(func):
    async def wrapper(message: Message, *args, **kwargs):
        service_name = message.text
        if not (4 <= len(service_name) <= 30):
            await message.answer(
                text="Назва послуги повинна бути від 3 до 30 символів.\nСпробуйте ще раз."
            )
            return

        if not re.match(r"^[A-Za-zА-Яа-яЁёЇїІіЄєҐґ+\- ]+$", service_name):
            await message.answer(
                "Назва послуги може містити тільки букви, пробіли, плюс та дефіс.\nСпробуйте ще раз."
            )
            return
        existing_service = await services_manager.read(name=service_name)
        if existing_service:
            await message.answer(
                text=f"Послуга - {service_name} вже існує.\nСпробуйте Ще раз."
            )
            return

        await func(message, service_name, *args, **kwargs)

    return wrapper


def validate_service_price(func):
    async def wrapper(message: Message, *args, **kwargs):
        try:
            price = int(message.text)
        except ValueError:
            await message.answer(
                text="Вартість повинна бути числом.\nСпробуйте ще раз."
            )
            return

        if price <= 0:
            await message.answer(
                text="Вартість повинна бути додатнім числом.\nСпробуйте ще раз."
            )
            return

        await func(message, price, *args, **kwargs)

    return wrapper


def validate_service_duration(func):
    async def wrapper(message: Message, *args, **kwargs):
        try:
            durations = timedelta(minutes=int(message.text))
        except ValueError:
            await message.answer(
                text="Тривалість повинна бути числом.\nСпробуйте ще раз."
            )
            return

        if durations <= timedelta(hours=0):
            await message.answer(
                text="Тривалість повинна бути додатнім числом. \nСпробуйте ще раз."
            )
            return

        await func(message, durations, *args, **kwargs)
        return True

    return wrapper


def validate_date(func):
    async def wrapper(message: Message, *args, **kwargs):
        logger.info("Запуск декоратора для валідації нової дати")
        date = message.text
        logger.info(f"Date: {date} | type: {type(date)}")
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", date):
            await message.answer(
                "Дата повинна бути у форматі YYYY-MM-DD. \nПриклад: 1900-01-01."
            )
            return

        date = datetime.strptime(date, "%Y-%m-%d").date()
        if date < datetime.now().date():
            await message.answer(
                "Дата повинна бути більшою або дорівнювати поточній даті. \nСпробуйте ще раз."
            )
            return
        dates = await dates_manager.read(date=date)
        if dates:
            await message.answer(
                text=f"Дата - {date} вже є в списку. \nСпробуйте ще раз"
            )
            return
        date = datetime.combine(date, time(18, 0))
        await func(message, date, *args, **kwargs)
        return True

    return wrapper


def block_if_booked(field_id: str):
    def decorator(func):
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            logger.info("Запуск декоратора для перевірки бронювання")
            id_value = int(callback.data.split("_")[2])
            notes = await notes_manager.read(
                **{field_id: id_value, "active": True},
            )
            user_ids = ()
            if notes:
                user_ids = tuple(note.user_id for note in notes)
            if user_ids:
                keyboard = await delete_booking_keyboard(
                    field=field_id, id_value=id_value, user_ids=user_ids
                )
                msg = template_manager.get_warning_del_date_or_service()
                await callback.message.answer(text=msg, reply_markup=keyboard)
                await callback.answer()
                return

            await func(callback, id_value, *args, **kwargs)

        return wrapper

    return decorator
