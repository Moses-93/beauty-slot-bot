from aiogram import F, Router
from punq import Container

from src.bot.client.states.booking import BookingStates
from src.bot.client.handlers.booking import BookingHandler
from src.bot.shared.filters.user import RoleFilter
from src.domain.enums.user_role import UserRole
from src.bot.shared.routers.base import BaseRouter


class BookingRouter(BaseRouter):
    def __init__(self, container: Container):
        self.handler = BookingHandler(container)
        super().__init__(Router())

    def _register(self):
        self.router.message.register(
            self.handler.make_appointment,
            F.text == "📝 Записатися",
            RoleFilter(roles={UserRole.CLIENT}),
        )
        self.router.callback_query.register(
            self.handler.handle_set_service, BookingStates.service
        )
        self.router.callback_query.register(
            self.handler.handle_set_date, BookingStates.date
        )
        self.router.message.register(self.handler.handle_set_time, BookingStates.time)
        self.router.message.register(
            self.handler.handle_set_reminder, BookingStates.reminder
        )
        self.router.callback_query.register(
            self.handler.handle_confirm, BookingStates.confirm
        )
