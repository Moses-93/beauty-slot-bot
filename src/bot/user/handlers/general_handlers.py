import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.utils.formatted_view import ViewController
from src.utils.message_templates import template_manager

from src.bot.user.keyboards import general_keyboards, booking_keyboard

from src.db.crud import dates_manager, services_manager


logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start(message: Message, user_id):
    logger.info(f"USER_ID - {user_id}")
    msg = template_manager.get_greeting_message()
    await message.answer(text=msg, reply_markup=general_keyboards.main_keyboard)


@router.message(lambda message: message.text == "Записатись")
async def make_an_appointment(message: Message, *args, **kwargs):
    services = await services_manager.read()
    msg = template_manager.get_service_options()
    service = await booking_keyboard.services_keyboard(act="service", services=services)
    await message.answer(text=msg, reply_markup=service)
    return


@router.message(lambda message: message.text == "Мої записи")
async def show_notes(message: Message):
    msg = template_manager.get_entry_options()
    await message.answer(text=msg, reply_markup=booking_keyboard.notes)
    return


@router.message(lambda message: message.text == "Доступні послуги")
async def show_services(message: Message, *args, **kwargs):
    services = await services_manager.read()
    if not services:
        await message.answer(text="Немає доступних послуг.")
        return
    formatted_service = ViewController(services=services).get()

    await message.answer(text=formatted_service, parse_mode="Markdown")


@router.message(lambda message: message.text == "Доступні дати")
async def show_dates(message: Message, *args, **kwargs):
    free_dates = await dates_manager.read(free=True)
    if not free_dates:
        await message.answer(text="Немає доступних дат.")
        return
    formatted_date = ViewController(dates=free_dates).get()
    await message.answer(text=formatted_date, parse_mode="Markdown")
    return


@router.message(lambda message: message.text == "Контакти")
async def show_contacts(message: Message):
    msg = template_manager.get_contacts_info()
    await message.answer(text=msg, parse_mode="Markdown")
