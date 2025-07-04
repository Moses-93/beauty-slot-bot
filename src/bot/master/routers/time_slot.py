from aiogram import Router, F
from punq import Container

from src.bot.master.states.time_slot import CreateTimeSlotStates, CancelTimeSlotStates
from src.bot.master.handlers.time_slot import (
    CreateTimeSlotHandler,
    CancelTimeSlotHandler,
)
from src.bot.master.filters.time_slot import DateValidatorFilter, TimeValidatorFilter
from src.bot.shared.routers.base import BaseRouter
from src.bot.shared.filters.user import RoleFilter
from src.domain.enums.user_role import UserRole


class TimeSlotRouter(BaseRouter):
    def __init__(self, container: Container):
        self._c_handler = CreateTimeSlotHandler(container)
        self._d_handler = CancelTimeSlotHandler(container)
        super().__init__(router=Router(name="date"))

    def _register(self):
        self.router.message.register(
            self._c_handler.handle_add_time_slot,
            F.text == "➕ Додати дату",
            RoleFilter(roles=UserRole.MASTER),
        )

        self.router.message.register(
            self._d_handler.handle_start_cancel_time_slot,
            F.text == "➖ Видалити дату",
            RoleFilter(roles=UserRole.MASTER),
        )

        self.router.message.register(
            self._c_handler.handle_set_date,
            CreateTimeSlotStates.date,
            DateValidatorFilter(),
        )
        self.router.message.register(
            self._c_handler.handle_set_start_time,
            CreateTimeSlotStates.start_time,
            TimeValidatorFilter(),
        )

        self.router.message.register(
            self._c_handler.handle_set_end_time,
            CreateTimeSlotStates.end_time,
            TimeValidatorFilter(),
        )

        self.router.callback_query.register(
            self._d_handler.handle_cancel_time_slot,
            CancelTimeSlotStates.time_slot_id,
        )
