import logging
from punq import Container
from aiogram.types import Message

from src.bot.master.keyboard.section import SectionKeyboards
from src.bot.master.messages.section import SectionMessages


class SectionHandler:
    def __init__(self, container: Container):
        self.container = container

    async def show_sections(self, message: Message):
        await message.answer(
            text=SectionMessages.start(), reply_markup=SectionKeyboards.main()
        )

    async def show_time_slots_section(self, message: Message):
        await message.answer(
            text=SectionMessages.time_slots(), reply_markup=SectionKeyboards.time_slots()
        )

    async def show_services_section(self, message: Message):
        await message.answer(
            text=SectionMessages.services(),
            reply_markup=SectionKeyboards.services(),
        )

    async def show_contacts_section(self, message: Message):
        await message.answer(
            text=SectionMessages.contacts(),
            reply_markup=SectionKeyboards.contacts(),
        )
