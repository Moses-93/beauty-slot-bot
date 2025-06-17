from aiogram import F, Router
from aiogram.filters import or_f
from punq import Container

from src.bot.shared.handlers.booking import BookingDisplayHandler
from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.enums.pagination import PaginationCategory


class BookingDisplayRouter:
    def __init__(self, container: Container):
        self._container = container
        self._router = Router()
        self._handler = BookingDisplayHandler(self._container)

    def register(self):
        self._router.callback_query.register(
            self._handler.show_active_bookings,
            F.data == "active_bookings",
        )
        self._router.callback_query.register(
            self._handler.show_all_bookings,
            F.data == "all_bookings",
        )
        self._router.callback_query.register(
            self._handler.paginate_bookings,
            or_f(
                PaginationCallback.filter(category=PaginationCategory.ACTIVE_BOOKINGS),
                PaginationCallback.filter(category=PaginationCategory.ALL_BOOKINGS),
            ),
        )

    @property
    def router(self) -> Router:
        return self._router
