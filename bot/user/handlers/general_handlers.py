import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from db.db_reader import GetService
from utils.formatted_view import format_services
from user_data import set_user_data
from utils.message_templates import template_manager


from bot.user.keyboards import general_keyboards, booking_keyboard

general_router = Router()
logger = logging.getLogger(__name__)


@general_router.message(CommandStart())
async def start(message: Message, user_id):
    set_user_data(user_id)
    logger.info(f"USER_ID - {user_id}")
    msg = template_manager.get_greeting_message()
    await message.answer(text=msg, reply_markup=general_keyboards.main_keyboard)


@general_router.message(lambda message: message.text == "Записатись")
async def make_an_appointment(message: Message):
    msg = template_manager.get_service_options()
    service = await booking_keyboard.services_keyboard("service")
    await message.answer(text=msg, reply_markup=service)
    return


@general_router.message(lambda message: message.text == "Мої записи")
async def show_notes(message: Message):
    msg = template_manager.get_entry_options()
    await message.answer(text=msg, reply_markup=booking_keyboard.notes)
    return


@general_router.message(lambda message: message.text == "Послуги")
async def show_services(message: Message):
    service = await GetService(all_services=True).get()
    formatted_service = format_services(service)

    await message.answer(text=formatted_service, parse_mode="Markdown")


@general_router.message(lambda message: message.text == "Контакти")
async def show_contacts(message: Message):
    msg = template_manager.get_contacts_info()
    await message.answer(text=msg, parse_mode="Markdown")
