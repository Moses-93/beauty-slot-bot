import logging
from punq import Container
from aiogram.types import Message

from src.application.use_cases.contact import GetContactsUseCase
from src.bot.shared.formatters.contact import ContactFormatter

logger = logging.getLogger(__name__)


class ContactDisplayHandler:
    def __init__(self, container: Container):
        self._container = container
        self._contact_uc: GetContactsUseCase = container.resolve(GetContactsUseCase)
        self.formatter = ContactFormatter(parse_mode="HTML")

    async def show_contact(self, message: Message):
        result = await self._contact_uc()
        if result.is_success:
            text = self.formatter.format(result.data)
            await message.answer(text=text)
        else:
            await message.answer(
                result.message or "Упс, щось пішло не так!"
            )  # TODO: Add production ready message
