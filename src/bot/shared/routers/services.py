from aiogram import F, Router
from punq import Container

from src.bot.shared.handlers.service import ServiceDisplayHandler
from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.enums.pagination import PaginationCategory


class ContactDisplayRouter:
    def __init__(self, container: Container):
        self._container = container
        self._router = Router()
        self._handler = ServiceDisplayHandler(self._container)

    def register(self):
        self._router.message.register(
            self._handler.show_services,
            F.text.in_("📋 Послуги", "📋 Список послуг"),
        )

        self._router.callback_query.register(
            self._handler.paginate_service,
            PaginationCallback.filter(category=PaginationCategory.SERVICES),
        )

    @property
    def router(self) -> Router:
        return self._router
