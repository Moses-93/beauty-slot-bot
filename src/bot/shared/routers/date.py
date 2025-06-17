from aiogram import F, Router
from punq import Container

from src.bot.shared.handlers.date import DateDisplayHandler
from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.enums.pagination import PaginationCategory


class ContactDisplayRouter:
    def __init__(self, container: Container):
        self._container = container
        self._router = Router()
        self._handler = DateDisplayHandler(self._container)

    def register(self):
        self._router.message.register(
            self._handler.show_dates,
            F.text.in_("🗓 Доступні дати", "📅 Список дат"),
        )

        self._router.callback_query.register(
            self._handler.paginate_dates,
            PaginationCallback.filter(category=PaginationCategory.DATES),
        )

    @property
    def router(self) -> Router:
        return self._router
