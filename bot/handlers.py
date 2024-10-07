import re
import logging


from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from .keyboards import services_keyboard, free_dates_keyboard
from utils.db import session, Service, FreeDate
from utils.utils import handlers_time, add_notes
from functools import wraps


logger = logging.getLogger(__name__)

# Установка рівня логування
logging.basicConfig(
    level=logging.DEBUG,  # Можна змінити на DEBUG для виведення більшої кількості інформації
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(),  # Виведення в консоль
    ],
)


def check_user_data(func):
    @wraps(func)
    async def wrapper(message, *args, **kwargs):
        user_id = message.from_user.id
        if user_id not in user_data:
            await message.answer("Виберіть послугу й дату з першого пункту меню.")
            return
        return await func(message, *args, **kwargs)
    return wrapper


router = Router()

user_data = {}


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text="Вітаю. \nЯ - сертифікований майстер-бровіст Дарія.\n"
        "Надаю професійні послуги з догляду за бровами.\n"
        "Оберіть будь ласка послугу:",
        reply_markup=services_keyboard,
    )

@check_user_data
@router.callback_query(lambda c: c.data.startswith("service_"))
async def handle_services(callback: CallbackQuery):
    service_id = int(callback.data.split("_")[1])
    service = session.query(Service).get(service_id)

    if service is None:
        await callback.message.answer("Вибрана послуга не знайдена. Спробуйте ще раз.")
        await callback.answer()
        return

    await callback.message.answer(
        f"Ви обрали '{service.name}'. Вартість: {service.price} грн. \nОберіть дату, на яку бажаєте записатись",
        reply_markup=free_dates_keyboard,
    )
    user_id = callback.from_user.id
    user_data[user_id] = {"service": service}
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("date_"))
async def selected_date_handler(callback: CallbackQuery):
    date_id = int(callback.data.split("_")[1])
    date = session.query(FreeDate).get(date_id)

    if date is None:
        await callback.message.answer("Вибрана дата не знайдена. Спробуйте ще раз.")
        await callback.answer()
        return

    await callback.message.answer(
        f"Ви обрали дату '{date.date}'. Напишіть час, на який ви бажаєте записатись в діапазоні 10:00-18:00 у форматі 'ГГ:ХХ'"
    )
    user_id = callback.from_user.id
    user_data[user_id]["date"] = date
    await callback.answer()


time_pattern = r"^(1[0-7]:[0-5]\d|18:00)$"
@check_user_data
@router.message(F.text.regexp(time_pattern))
async def accepts_time(message: Message):
    logger.debug("Запуск обробника часу")  # Логування початку виконання функції
    user_id = message.from_user.id

    logger.info(f"User {message.from_user.full_name} selected time: {message.text}")

    name = message.from_user.first_name
    username = message.from_user.username
    time = message.text
    handlers = handlers_time(name, username, time, user_id, user_data)
    if handlers is None:
        await message.answer(
            text=f"{name}, Ви успішно записались на послугу - {user_data[user_id]['service'].name}\n Чекаю на Вас {user_data[user_id]['date'].date} о {time}"
        )
        user_data.pop(
            user_id
        )  # Видалення з user_data, коли запис на замовлення створено
    else:
        message_text, keyboard = handlers
        await message.answer(text=message_text, reply_markup=keyboard)


@check_user_data
@router.callback_query(lambda c: c.data.startswith('confirm_'))
async def confirm_the_entry(callback: CallbackQuery):
    user_id = callback.from_user.id
    time = callback.data.split('_')[-1]
    name = callback.from_user.first_name
    username = callback.from_user.username
    date = user_data[user_id].get("date")
    service = user_data[user_id]['service']
    add_notes(name, username, time, date.date, service)
    await callback.message.answer(f"Ви успішно записались на послугу - {service}. \nЧекаю на Вас {date} о {time}")
    user_data.pop(user_id)