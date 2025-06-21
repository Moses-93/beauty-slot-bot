from aiogram import Router
from aiogram.filters import CommandStart

from src.bot.shared.routers.base import BaseRouter
from src.bot.master.handlers.start import StartHandler
from src.bot.shared.filters.user import RoleFilter
from src.domain.enums.user_role import UserRole


class StartRouter(BaseRouter):
    def __init__(self):
        self._handler = StartHandler()
        super().__init__(router=Router())

    def _register(self):
        self.router.message.register(
            self._handler.show_sections,
            CommandStart,
            RoleFilter(roles={UserRole.MASTER}),
        )
