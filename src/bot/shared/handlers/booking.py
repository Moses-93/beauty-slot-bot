import logging
from punq import Container
from aiogram.types import CallbackQuery

from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.handlers.base import BaseDisplayHandler
from src.bot.shared.formatters.booking import BookingFormatter
from src.bot.shared.enums.pagination import PaginationCategory
from src.application.use_cases.booking import GetBookingUseCase
from src.domain.entities.user import User

logger = logging.getLogger(__name__)


class BookingDisplayHandler(BaseDisplayHandler):
    def __init__(self, container: Container):
        super().__init__(
            container=container,
            formatter=BookingFormatter(parse_mode="HTML"),
        )
        self._booking_uc: GetBookingUseCase = self.resolve(GetBookingUseCase)

    async def show_all_bookings(self, callback: CallbackQuery, user: User):
        await self._show_bookings(
            callback=callback,
            user=user,
            is_active=False,
            category=PaginationCategory.ALL_BOOKINGS,
        )

    async def show_active_bookings(self, callback: CallbackQuery, user: User):
        await self._show_bookings(
            callback=callback,
            user=user,
            is_active=True,
            category=PaginationCategory.ACTIVE_BOOKINGS,
        )

    async def paginate_bookings(
        self, callback: CallbackQuery, callback_data: PaginationCallback, user: User
    ):
        limit = callback_data.limit
        offset = callback_data.offset
        is_active = callback_data.category == PaginationCategory.ACTIVE_BOOKINGS

        result = await self._booking_uc(
            user=user, is_active=is_active, limit=limit + 1, offset=offset
        )

        if result.is_success:
            await self.edit_page(
                callback=callback,
                items=result.data,
                category=callback_data.category,
                limit=limit,
                offset=offset,
            )
        else:
            await callback.message.answer(
                result.message or "Упс, щось пішло не так!"
            )  # TODO: Add a production ready message

    async def _show_bookings(
        self,
        callback: CallbackQuery,
        user: User,
        is_active: bool,
        category: PaginationCategory,
    ):
        result = await self._booking_uc(
            user=user, is_active=is_active, limit=6, offset=0
        )
        if result.is_success:
            await self.send_page(
                message=callback.message,
                items=result.data,
                category=category,
                limit=5,
                offset=0,
            )
        else:
            await callback.message.answer(
                result.message
                or "Упс, щось пішло не так!"  # TODO: Add a production ready message
            )
