from aiogram.types import Message

from src.bot.client.keyboard.section import SectionKeyboards
from src.bot.client.messages.section import SectionMessages


class StartHandler:

    async def show_sections(self, message: Message):
        await message.answer(
            text=SectionMessages.main(), reply_markup=SectionKeyboards.main()
        )
