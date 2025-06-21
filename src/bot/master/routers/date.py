from aiogram import Router, F
from punq import Container

from src.bot.master.states.date import CreateDateStates, DeactivateDateStates
from src.bot.master.handlers.date import CreateDateHandler, DeactivateDateHandler
from src.bot.master.filters.date import DateValidatorFilter, TimeValidatorFilter
from src.bot.shared.routers.base import BaseRouter
from src.bot.shared.filters.user import RoleFilter
from src.domain.enums.user_role import UserRole


class DateRouter(BaseRouter):
    def __init__(self, container: Container):
        self._c_handler = CreateDateHandler(container)
        self._d_handler = DeactivateDateHandler(container)
        super().__init__(router=Router(name="date"))

    def _register(self):
        self.router.message.register(
            self._c_handler.handle_start_add_date,
            F.text == "➕ Додати дату",
            RoleFilter(roles=UserRole.MASTER),
        )

        self.router.message.register(
            self._d_handler.handle_start_deactivate_date,
            F.text == "➖ Видалити дату",
            RoleFilter(roles=UserRole.MASTER),
        )

        self.router.message.register(
            self._c_handler.handle_set_date,
            CreateDateStates.date,
            DateValidatorFilter(),
        )
        self.router.message.register(
            self._c_handler.handle_set_deactivation_time,
            CreateDateStates.deactivation_time,
            TimeValidatorFilter(),
        )

        self.router.callback_query.register(
            self._d_handler.handle_delete_date,
            DeactivateDateStates.date_id,
        )
