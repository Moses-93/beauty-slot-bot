import re
import logging
from datetime import datetime, time
from utils.format_datetime import FormatDate
from aiogram.types import Message
from db.db_reader import get_date


logger = logging.getLogger(__name__)


def validator_date(func):
    async def wrapper(message: Message, *args, **kwargs):
        logger.info("Запуск декоратора для валідації нової дати")
        date = message.text
        logger.info(f"Date: {date} | type: {type(date)}")
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", date):
            await message.answer(
                "Дата повинна бути у форматі YYYY-MM-DD. \nПриклад: 1900-01-01."
            )
            return

        date = FormatDate().formats_date_str_to_datetime(date).date()
        if date < datetime.now().date():
            await message.answer(
                "Дата повинна бути більшою або дорівнювати поточній даті. \nСпробуйте ще раз."
            )
            return
        dates = await get_date.get_date(first=True, date=date)
        if dates:
            await message.answer(
                text=f"Дата - {date} вже є в списку. \nСпробуйте ще раз"
            )
            return
        date = datetime.combine(date, time(18, 0))
        await func(message, date, *args, **kwargs)
        return True

    return wrapper
