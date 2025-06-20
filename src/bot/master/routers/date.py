from aiogram import Router, F
from punq import Container

from src.bot.master.states.date import CreateDateStates, DeactivateDateStates
from src.bot.master.handlers.date import CreateDateHandler, DeactivateDateHandler
from src.bot.master.filters.date import DateValidatorFilter, TimeValidatorFilter
from src.bot.shared.routers.base import BaseRouter
from src.bot.shared.filters.user import RoleFilter
from src.domain.enums.user_role import UserRole

_date_router = Router()


class CreateDateRouter(BaseRouter):
    def __init__(self, container: Container):
        self.handler = CreateDateHandler(container)
        super().__init__(router=_date_router)

    def _register(self):
        self.router.message.register(
            self.handler.handle_start_add_date,
            F.text == "➕ Додати дату",
            RoleFilter(roles=UserRole.MASTER),
        )

        self.router.message.register(
            self.handler.handle_set_date, CreateDateStates.date, DateValidatorFilter()
        )
        self.router.message.register(
            self.handler.handle_set_deactivation_time,
            CreateDateStates.deactivation_time,
            TimeValidatorFilter(),
        )


class DeactivateDateRouter(BaseRouter):
    def __init__(self, container: Container):
        self.handler = DeactivateDateHandler(container)
        super().__init__()

    def _register(self):
        self.router.message(F.text == "➖ Видалити дату")(
            self.handler.handle_start_deactivate_date, RoleFilter(roles=UserRole.MASTER)
        )
        self.router.callback_query.register(
            self.handler.handle_delete_date,
            DeactivateDateStates.date_id,
        )
