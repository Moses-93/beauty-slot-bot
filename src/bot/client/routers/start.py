from aiogram import Router
from aiogram.filters import CommandStart

from src.bot.shared.routers.base import BaseRouter
from src.bot.client.handlers.start import StartHandler
from src.bot.shared.filters.user import RoleFilter
from src.domain.enums.user_role import UserRole


class StartRouter(BaseRouter):
    def __init__(self):
        super().__init__(router=Router())
        self._handler = StartHandler()

    def _register(self):
        self._router.message.register(
            self._handler.show_sections,
            CommandStart,
            RoleFilter(roles={UserRole.CLIENT}),
        )
