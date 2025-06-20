from aiogram.types import Message

from src.bot.master.keyboard.section import SectionKeyboards
from src.bot.master.messages.section import SectionMessages


class StartHandler:

    async def show_sections(self, message: Message):
        await message.answer(
            text=SectionMessages.start(), reply_markup=SectionKeyboards.main()
        )
