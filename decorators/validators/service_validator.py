import logging
import re
from aiogram.types import Message
from datetime import timedelta

from db.db_reader import GetService

logger = logging.getLogger(__name__)


def validate_service_name(func):
    async def wrapper(message: Message, *args, **kwargs):
        service_name = message.text
        logger(f"NAME: {service_name}")
        existing_service = GetService(name=service_name).get_service_by_name()
        if existing_service:
            await message.answer(
                text="Така назва послуги вже існує.\nСпробуйте Ще раз."
            )
            return
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


def validate_service_durations(func):
    async def wrapper(message: Message, *args, **kwargs):
        try:
            durations = int(message.text)
            durations = timedelta(minutes=durations)
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

    return wrapper
