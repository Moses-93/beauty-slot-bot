from aiogram import Router, F
from punq import Container

from src.bot.master.handlers import service
from src.bot.master.states.service import (
    CreateServiceStates,
    DeleteServiceStates,
    UpdateServiceStates,
)
from src.bot.master.routers.base import BaseRouter
from src.bot.master.filters.service import (
    TitleValidatorFilter,
    PriceValidatorFilter,
    DurationValidatorFilter,
)


_service_router = Router(name="service")


class CreateServiceRouter(BaseRouter):
    def __init__(self, container: Container):
        self._handler = service.CreateServiceHandler(container)
        super().__init__(_router=_service_router)

    def _register(self):
        self._router.message.register(
            self._handler.handle_start, F.text == "➕ Додати послугу"
        )

        self._router.message.register(
            self._handler.handle_set_title,
            CreateServiceStates.title,
            TitleValidatorFilter(),
        )

        self._router.message.register(
            self._handler.handle_set_price,
            CreateServiceStates.price,
            PriceValidatorFilter(),
        )

        self._router.message.register(
            self._handler.handle_set_duration,
            CreateServiceStates.duration,
            DurationValidatorFilter(),
        )


class DeactivateServiceRouter(BaseRouter):
    def __init__(self, container: Container):
        self._handler = service.DeactivateServiceHandler(container)
        super().__init__(_router=_service_router)

    def _register(self):
        self._router.message.register(
            self._handler.show_service, F.text == "➖ Видалити послугу"
        )

        self._router.callback_query.register(
            self._handler.handle_set_selected_service, DeleteServiceStates.service_id
        )


class EditServiceRouter(BaseRouter):
    def __init__(self, container: Container):
        self._handler = service.EditServiceHandler(container)
        super().__init__(_router=_service_router)

    def _register(self):
        self._router.message.register(
            self._handler.show_service, F.text == "🔄 Оновити послугу"
        )

        self._router.callback_query.register(
            self._handler.handle_set_selected_service,
            UpdateServiceStates.service_id,
        )

        self._router.callback_query.register(
            self._handler.handle_set_selected_field,
            UpdateServiceStates.field,
        )

        self._router.message.register(
            self._handler.handle_set_new_value, UpdateServiceStates.value
        )
