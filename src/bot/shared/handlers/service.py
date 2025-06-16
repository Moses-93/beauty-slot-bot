import logging
from punq import Container
from aiogram.types import Message, CallbackQuery

from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.handlers.base import BaseDisplayHandler
from src.application.use_cases.service import GetServicesUseCase
from src.bot.shared.formatters.service import ServiceFormatter
from src.bot.shared.enums.pagination import PaginationCategory


logger = logging.getLogger(__name__)


class ServiceDisplayHandler(BaseDisplayHandler):
    def __init__(self, container: Container):
        super().__init__(container)
        self._service_uc: GetServicesUseCase = self.resolve(GetServicesUseCase)
        self.category = PaginationCategory.SERVICES
        self._formatter = ServiceFormatter(parse_mode="HTML")

    async def show_services(self, message: Message):
        result = await self._service_uc(limit=5 + 1, offset=0)
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
                result.message or "Щось пішло не так"
            )  # TODO: Add a production ready message

    async def paginate_service(
        self, callback: CallbackQuery, callback_data: PaginationCallback
    ):
        limit = callback_data.limit
        offset = callback_data.offset
        result = await self._service_uc(limit=limit + 1, offset=offset)
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
                result.message or "Щось пішло не так", show_alert=True
            )  # TODO: Add a production ready message
