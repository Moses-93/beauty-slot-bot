from datetime import timedelta
import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from .keyboards import services_keyboard, free_dates_keyboard
from utils.db import get_free_date, get_service
from utils.format_datetime import NowDatetime
from utils.utils import handlers_time, add_notes, get_service, get_user_data
from decorators.check_user_data import check_user_id
from user_data import user_data, get_user_data, set_user_data

logger = logging.getLogger(__name__)

# Установка рівня логування
# logging.basicConfig(
#     level=logging.DEBUG,  # Можна змінити на DEBUG для виведення більшої кількості інформації
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler("logs/bot.log"),
#         logging.StreamHandler(),  # Виведення в консоль
#     ],
# )


router = Router()
current_datetime = NowDatetime()


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    set_user_data(
        user_id, name=message.from_user.first_name, username=message.from_user.username
    )
    logger.info(f"USER_DATA(start) --- {user_data}")
    await message.answer(
        text="Вітаю. \nЯ - сертифікований майстер-бровіст Дарія.\n"
        "Надаю професійні послуги з догляду за бровами.\n"
        "Оберіть будь ласка послугу:",
        reply_markup=services_keyboard,
    )


@check_user_id
@router.callback_query(lambda c: c.data.startswith("service_"))
async def processes_services(callback: CallbackQuery):
    service_id = int(callback.data.split("_")[1])
    service = get_service(service_id)
    logger.info(f"Selected date: {service.name}. Type:{type(service.name)}")

    await callback.message.answer(
        f"Ви обрали '{service.name}'. Вартість: {service.price} грн. \nОберіть дату, на яку бажаєте записатись",
        reply_markup=free_dates_keyboard,
    )
    user_id = callback.from_user.id
    set_user_data(user_id, service=service)
    logger.info(f"USER_DATA(handle_services) --- {user_data}")
    await callback.answer()


@check_user_id
@router.callback_query(lambda c: c.data.startswith("date_"))
async def processes_dates(callback: CallbackQuery):
    date_id = int(callback.data.split("_")[1])
    date = get_free_date(date_id)
    logger.info(f"Selected date: {date.date}. Type:{type(date.date)}")

    await callback.message.answer(
        f"Ви обрали дату '{date.date}'. Напишіть час до 18:00 у форматі 'ГГ:ХХ'"
    )
    user_id = callback.from_user.id
    set_user_data(user_id, date=date)
    logger.info(f"USER_DATA(date_handler)---{user_data}")
    await callback.answer()


time_pattern = r"^(1[0-7]:[0-5]\d|18:00)$"


@check_user_id
@router.message(F.text.regexp(time_pattern))
async def processes_time(message: Message):
    logger.debug("Запуск обробника часу")  # Логування початку виконання функції
    user_id = message.from_user.id
    time = message.text
    logger.info(f"User {message.from_user.full_name} selected time: {time}")

    handlers = handlers_time(user_id, time)
    if handlers is None:
        user = get_user_data(user_id, "name", "service", "date")
        await message.answer(
            text=f"{user.get('name')}, Ви успішно записались на послугу - {user.get('service').name}\n Чекаю на Вас {user.get('date').date} о {time}"
        )
        user_data.pop(user_id)
    elif handlers[0] == False:
        _, msg = handlers
        await message.answer(text=msg)
    else:
        message_text, keyboard = handlers
        await message.answer(text=message_text, reply_markup=keyboard)


@check_user_id
@router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_the_entry(callback: CallbackQuery):
    user_id = callback.from_user.id
    time = callback.data.split("_")[-1]
    user = get_user_data(user_id, "name", "username", "date", "service")
    add_notes(
        user.get("name"),
        user.get("username"),
        time,
        user.get("date"),
        user.get("service"),
    )
    await callback.message.answer(
        f"Ви успішно записались на послугу - {user.get('service').name}. \nЧекаю на Вас {user.get('date').date} о {time}"
    )
    user_data.pop(user_id)
