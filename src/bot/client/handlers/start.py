from aiogram.types import Message

from src.domain.entities.user import User
from src.bot.client.keyboard.section import SectionKeyboards
from src.bot.client.messages.section import SectionMessages


class StartHandler:

    async def show_sections(self, message: Message, user: User):
        await message.answer(
            text=SectionMessages.main(user.name or user.username),
            reply_markup=SectionKeyboards.main(),
        )
