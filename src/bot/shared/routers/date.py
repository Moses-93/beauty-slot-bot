from aiogram import F, Router
from punq import Container

from src.bot.shared.handlers.date import DateDisplayHandler
from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.enums.pagination import PaginationCategory
from src.bot.shared.routers.base import BaseRouter


class DateDisplayRouter(BaseRouter):
    def __init__(self, container: Container):
        self._handler = DateDisplayHandler(container)
        super().__init__(Router())

    def register(self):
        self.router.message.register(
            self._handler.show_dates,
            F.text.in_("🗓 Доступні дати", "📅 Список дат"),
        )

        self.router.callback_query.register(
            self._handler.paginate_dates,
            PaginationCallback.filter(category=PaginationCategory.DATES),
        )
