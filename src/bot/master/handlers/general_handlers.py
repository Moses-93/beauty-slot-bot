import logging
from aiogram.types import Message

from src.bot.keyboard.master import MasterKeyboard
from src.bot.messages.master import MasterMessages

logger = logging.getLogger(__name__)


class MenuHandler:

    async def show_main_menu(self, message: Message):
        await message.answer(
            text=MasterMessages.start(),
            reply_markup=MasterKeyboard.main_section(),
        )

    async def show_services_menu(self, message: Message):
        await message.answer(
            text=MasterMessages.services_menu(),
            reply_markup=MasterKeyboard.services_section(),
        )

    async def show_dates_menu(self, message: Message):
        await message.answer(
            text=MasterMessages.dates_menu(),
            reply_markup=MasterKeyboard.dates_section(),
        )

    async def show_bookings_menu(self, message: Message):
        await message.answer(
            text=MasterMessages.bookings_menu(),
            reply_markup=MasterKeyboard.bookings_section(),
        )
