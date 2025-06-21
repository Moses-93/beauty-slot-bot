from aiogram import Router, F
from punq import Container

from src.bot.master.handlers import service
from src.bot.master.states.service import (
    CreateServiceStates,
    DeleteServiceStates,
    UpdateServiceStates,
)
from src.bot.shared.routers.base import BaseRouter
from src.bot.master.filters.service import (
    TitleValidatorFilter,
    PriceValidatorFilter,
    DurationValidatorFilter,
)
from src.bot.shared.filters.user import RoleFilter
from src.domain.enums.user_role import UserRole


class ServiceRouter(BaseRouter):
    def __init__(self, container: Container):
        self._c_handler = service.CreateServiceHandler(container)
        self._d_handler = service.DeactivateServiceHandler(container)
        self._e_handler = service.EditServiceHandler(container)
        super().__init__(router=Router(name="service"))

    def _register(self):
        self.router.message.register(
            self._c_handler.handle_start,
            F.text == "➕ Додати послугу",
            RoleFilter(UserRole.MASTER),
        )

        self.router.message.register(
            self._d_handler.show_service,
            F.text == "➖ Видалити послугу",
            RoleFilter(UserRole.MASTER),
        )

        self.router.message.register(
            self._e_handler.show_service,
            F.text == "🔄 Оновити послугу",
            RoleFilter(UserRole.MASTER),
        )

        self.router.message.register(
            self._c_handler.handle_set_title,
            CreateServiceStates.title,
            TitleValidatorFilter(),
        )

        self.router.message.register(
            self._c_handler.handle_set_price,
            CreateServiceStates.price,
            PriceValidatorFilter(),
        )

        self.router.message.register(
            self._c_handler.handle_set_duration,
            CreateServiceStates.duration,
            DurationValidatorFilter(),
        )

        self.router.callback_query.register(
            self._d_handler.handle_set_selected_service,
            DeleteServiceStates.service_id,
        )

        self.router.callback_query.register(
            self._e_handler.handle_set_selected_service,
            UpdateServiceStates.service_id,
        )

        self.router.callback_query.register(
            self._e_handler.handle_set_selected_field,
            UpdateServiceStates.field,
        )

        self.router.message.register(
            self._e_handler.handle_set_new_value,
            UpdateServiceStates.value,
        )
