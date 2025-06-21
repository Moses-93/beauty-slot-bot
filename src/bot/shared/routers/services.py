from aiogram import F, Router
from punq import Container

from src.bot.shared.handlers.service import ServiceDisplayHandler
from src.bot.shared.filters.pagination import PaginationCallback
from src.bot.shared.enums.pagination import PaginationCategory
from src.bot.shared.routers.base import BaseRouter


class ServiceDisplayRouter(BaseRouter):
    def __init__(self, container: Container):
        self._handler = ServiceDisplayHandler(container)
        super().__init__(Router())

    def _register(self):
        self.router.message.register(
            self._handler.show_services,
            F.text.in_("📋 Послуги", "📋 Список послуг"),
        )

        self.router.callback_query.register(
            self._handler.paginate_service,
            PaginationCallback.filter(category=PaginationCategory.SERVICES),
        )

    @property
    def router(self) -> Router:
        return self.router
