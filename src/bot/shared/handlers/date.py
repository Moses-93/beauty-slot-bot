import logging
from punq import Container
from aiogram.types import Message, CallbackQuery

from src.bot.shared.handlers.base import BaseDisplayHandler

from src.bot.shared.filters.pagination import PaginationCallback
from src.application.use_cases.date import GetAvailableDateUseCase
from src.bot.shared.formatters.date import DateFormatter
from src.bot.shared.enums.pagination import PaginationCategory

logger = logging.getLogger(__name__)


class DateDisplayHandler(BaseDisplayHandler):
    def __init__(self, container: Container):
        super().__init__(container)
        self._date_uc: GetAvailableDateUseCase = self.resolve(GetAvailableDateUseCase)
        self.category = PaginationCategory.DATES
        self._formatter = DateFormatter(parse_mode="HTML")

    async def show_dates(self, message: Message):
        result = await self._date_uc(5 + 1, 5)
        if result.is_success:
            await self.send_page(
                message=message,
                items=result.data,
                category=self.category,
                limit=5,
                offset=0,
            )
        else:
            await message.answer(
                result.message or "Упс, щось пішло не так"
            )  # TODO: Add a production ready message

    async def paginate_dates(
        self, callback: CallbackQuery, callback_data: PaginationCallback
    ):
        limit = callback_data.limit
        offset = callback_data.offset
        result = await self._date_uc(limit=limit + 1, offset=offset)
        if result.is_success:
            await self.edit_page(
                callback=callback,
                items=result.data,
                category=self.category,
                limit=limit,
                offset=offset,
            )
        else:
            await callback.answer(
                result.message or "Упс, щось пішло не так"
            )  # TODO: Add a production ready message
