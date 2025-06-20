from aiogram import Router, F
from punq import Container

from src.bot.master.handlers.navigation import SectionHandler
from src.bot.shared.filters.user import RoleFilter
from src.domain.enums.user_role import UserRole
from src.bot.shared.routers.base import BaseRouter


class SectionRouter(BaseRouter):
    def __init__(self, container: Container):
        self._handler = SectionHandler(container)
        super().__init__(Router(name="section"))

    def _register(self) -> None:
        self._router.message.register(self._handler.show_sections, CommandStart)
        self._router.message.register(
            self._handler.show_dates_section,
            F.text == "📅 Дати",
            RoleFilter({UserRole.MASTER}),
        )
        self._router.message.register(
            self._handler.show_services_section,
            F.text == "📖 Послуги",
            RoleFilter(roles={UserRole.MASTER}),
        )
        self._router.message.register(
            self._handler.show_booking_section,
            F.text == "📒 Записи",
            RoleFilter(roles={UserRole.MASTER}),
        )
