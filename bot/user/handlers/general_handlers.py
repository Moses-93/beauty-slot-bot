import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from decorators.caching.request_cache import get_all_service, get_free_dates
from utils.formatted_view import ViewController
from utils.message_templates import template_manager


from bot.user.keyboards import general_keyboards, booking_keyboard

general_router = Router()
logger = logging.getLogger(__name__)


@general_router.message(CommandStart())
async def start(message: Message, user_id):
    logger.info(f"USER_ID - {user_id}")
    msg = template_manager.get_greeting_message()
    await message.answer(text=msg, reply_markup=general_keyboards.main_keyboard)


@general_router.message(lambda message: message.text == "Записатись")
@get_all_service
async def make_an_appointment(message: Message, services, *args, **kwargs):
    msg = template_manager.get_service_options()
    service = await booking_keyboard.services_keyboard(act="service", services=services)
    await message.answer(text=msg, reply_markup=service)
    return


@general_router.message(lambda message: message.text == "Мої записи")
async def show_notes(message: Message):
    msg = template_manager.get_entry_options()
    await message.answer(text=msg, reply_markup=booking_keyboard.notes)
    return


@general_router.message(lambda message: message.text == "Доступні послуги")
@get_all_service
async def show_services(message: Message, services, *args, **kwargs):
    if not services:
        await message.answer(text="Немає доступних послуг.")
        return
    formatted_service = ViewController(services=services).get()

    await message.answer(text=formatted_service, parse_mode="Markdown")


@general_router.message(lambda message: message.text == "Доступні дати")
@get_free_dates
async def show_dates(message: Message, free_dates, *args, **kwargs):
    if not free_dates:
        await message.answer(text="Немає доступних дат.")
        return
    formatted_date = ViewController(dates=free_dates).get()
    await message.answer(text=formatted_date, parse_mode="Markdown")
    return


@general_router.message(lambda message: message.text == "Контакти")
async def show_contacts(message: Message):
    msg = template_manager.get_contacts_info()
    await message.answer(text=msg, parse_mode="Markdown")
