from aiogram import F, Router
from aiogram.filters import or_f
from punq import Container

from src.bot.shared.handlers.booking import BookingDisplayHandler
from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.enums.pagination import PaginationCategory
from src.bot.shared.routers.base import BaseRouter


class BookingDisplayRouter(BaseRouter):
    def __init__(self, container: Container):
        self._handler = BookingDisplayHandler(container)
        super().__init__(Router())

    def register(self):
        self.router.callback_query.register(
            self._handler.show_active_bookings,
            F.data == "active_bookings",
        )
        self.router.callback_query.register(
            self._handler.show_all_bookings,
            F.data == "all_bookings",
        )
        self.router.callback_query.register(
            self._handler.paginate_bookings,
            or_f(
                PaginationCallback.filter(category=PaginationCategory.ACTIVE_BOOKINGS),
                PaginationCallback.filter(category=PaginationCategory.ALL_BOOKINGS),
            ),
        )
