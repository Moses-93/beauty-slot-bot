import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from .keyboards import services_keyboard, free_dates_keyboard, main_keyboard
from db.commands import GetService, GetNotes, GetFreeDate
from db.queries import add_notes
from utils.format_datetime import NowDatetime
from utils.utils import handlers_time
from decorators.check_user_data import check_user_id
from user_data import get_user_data, set_user_data, user_data

logger = logging.getLogger(__name__)

router = Router()

current_datetime = NowDatetime()


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    set_user_data(
        user_id, name=message.from_user.first_name, username=message.from_user.username
    )
    logger.info(f"USER_DATA(start) --- {get_user_data(user_id)}")
    await message.answer(
        text="Вітаю. \nЯ - сертифікований майстер-бровіст Дарія.\n"
        "Надаю професійні послуги з догляду за бровами.\n"
        "Тут ви можете ознайомитись з послугами, цінами, та записатись",
        reply_markup=main_keyboard,
    )


@router.message(lambda message: message.text == "Записатись")
async def make_an_appointment(message: Message):
    msg = "Оберіть бажану послугу:"
    await message.answer(text=msg, reply_markup=services_keyboard)


@router.message(lambda message: message.text == "Мої записи")
async def show_contacts(message: Message):
    user_id = message.from_user.id

    notes = GetNotes(user_id=user_id).get_all_notes()
    if not notes:
        await message.answer(text="Нажаль я не зміг знайти ваші записи(")
        return
    formatted_notes = "\n\n".join([f"{i+1}: {note}" for i, note in enumerate(notes)])
    await message.answer(text=f"Ваші записи: \n\n{formatted_notes}")


@router.message(lambda message: message.text == "Послуги")
async def show_contacts(message: Message):
    formatted_service = "\n\n".join(
        [
            f"{i+1}: {service}"
            for i, service in enumerate(GetService().get_all_services())
        ]
    )

    await message.answer(text=f"Послуги:\n\n {formatted_service}")


@router.message(lambda message: message.text == "Контакти")
async def show_contacts(message: Message):
    msg = (
        "Адреса: [Вул. Перлинна 3](https://maps.app.goo.gl/coiRjcbFzwMTzppz8)\n"
        "Telegram: @chashurina\n"
        "Instagram: [chashurina_brows](https://www.instagram.com/chashurina_brows?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==)\n"
        "Телефон: +380934050798"
    )
    await message.answer(text=msg, parse_mode="Markdown")


@check_user_id
@router.callback_query(lambda c: c.data.startswith("service_"))
async def processes_services(callback: CallbackQuery):
    service_id = int(callback.data.split("_")[1])
    service = GetService(service_id)

    logger.info(f"Selected date: {service.name}. Type:{type(service.name)}")

    await callback.message.answer(
        f"Ви обрали '{service.name}'. Вартість: {service.price} грн. \nОберіть дату, на яку бажаєте записатись",
        reply_markup=free_dates_keyboard,
    )
    user_id = callback.from_user.id
    set_user_data(user_id, service=service)
    logger.info(f"USER_DATA(handle_services) --- {get_user_data(user_id)}")
    await callback.answer()


@check_user_id
@router.callback_query(lambda c: c.data.startswith("date_"))
async def processes_dates(callback: CallbackQuery):
    date_id = int(callback.data.split("_")[1])
    date = GetFreeDate(date_id)
    logger.info(f"Selected date: {date.date}. Type:{type(date.date)}")

    await callback.message.answer(
        f"Ви обрали дату '{date.date}'. Напишіть час до 18:00 у форматі 'ГГ:ХХ'"
    )
    user_id = callback.from_user.id
    set_user_data(user_id, date=date)
    logger.info(f"USER_DATA(date_handler)---{get_user_data(user_id)}")
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
        name, service, date = get_user_data(user_id, "name", "service", "date")
        await message.answer(
            text=f"{name}, Ви успішно записались на послугу - {service.name}\n Чекаю на Вас {date.date} о {time}"
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
    name, username, date, service = get_user_data(
        user_id, "name", "username", "date", "service"
    )
    add_notes(name, username, time, date, service, user_id)
    await callback.message.answer(
        f"Ви успішно записались на послугу - {service.name}. \nЧекаю на Вас {date.date} о {time}"
    )
    user_data.pop(user_id)
