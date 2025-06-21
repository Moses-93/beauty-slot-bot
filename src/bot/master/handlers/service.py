import logging
from punq import Container
from typing import Dict
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.master.states.service import (
    CreateServiceStates,
    DeleteServiceStates,
    UpdateServiceStates,
)
from src.shared.dto.result import ResultDTO
from src.bot.master.messages.service import ServiceMessage
from src.bot.shared.keyboard.display_data import DisplayData
from src.application.dto.service import ServiceDTO
from src.bot.master.messages.service import ServiceMessage
from src.application.use_cases.service import (
    CreateServiceUseCase,
    EditServiceUseCase,
    GetServicesUseCase,
)


logger = logging.getLogger(__name__)


class CreateServiceHandler:
    def __init__(self, container: Container):
        self._service_uc: CreateServiceUseCase = container.resolve(CreateServiceUseCase)

    async def handle_start(self, message: Message, state: FSMContext):
        await state.set_state(CreateServiceStates.title)
        await message.answer(
            text=ServiceMessage.enter_title(),
        )

    async def handle_set_title(self, message: Message, state: FSMContext, title: str):
        await state.update_data(title=title)
        await state.set_state(CreateServiceStates.price)

        await message.answer(text=ServiceMessage.enter_price())

    async def handle_set_price(self, message: Message, state: FSMContext, price: int):
        await state.update_data(price=price)
        await state.set_state(CreateServiceStates.duration)

        await message.answer(text=ServiceMessage.enter_duration())

    async def handle_set_duration(
        self, message: Message, state: FSMContext, duration: int
    ):
        state_data = await state.update_data(duration=duration)
        await self._add_service(message, state_data)
        await state.clear()

    async def _add_service(self, message: Message, raw_state_data: Dict):
        service_dto = ServiceDTO(**raw_state_data)
        result = await self._service_uc(service_dto)
        if result.is_success:
            await message.answer(
                text=ServiceMessage.success_create(
                    service_dto.title, service_dto.price, service_dto.duration
                )
            )
        else:
            await message.answer(text=ServiceMessage.fail_create())


class EditServiceHandler:
    def __init__(self, container: Container):
        self._get_service_us: GetServicesUseCase = container.resolve(GetServicesUseCase)
        self._edit_service_uc: EditServiceUseCase = container.resolve(
            EditServiceUseCase
        )

    async def show_service(self, message: Message, state: FSMContext):
        result = await self._get_service_us()
        keyboard = DisplayData.create_button(result.data, ("data",), ("id",))
        await state.set_state(UpdateServiceStates.service_id)
        await message.answer(text=ServiceMessage.edit(), reply_markup=keyboard)

    async def handle_set_selected_service(
        self, callback: CallbackQuery, state: FSMContext
    ):
        service_id = await callback.data
        await state.update_data(id=service_id)
        await state.set_state(UpdateServiceStates.field)
        keyboard = await self._build_keyboard()
        await callback.message.answer(
            text=ServiceMessage.select_field(), reply_markup=keyboard
        )

    async def handle_set_selected_field(
        self, callback: CallbackQuery, state: FSMContext
    ):
        field = callback.data
        await state.update_data(field=field)
        await state.set_state(UpdateServiceStates.value)
        await callback.message.answer(text=...)

    async def handle_set_new_value(
        self, message: Message, state: FSMContext, new_value
    ):
        state_data = await state.update_data(value=new_value)
        await self._edit_service(
            message, state_data["id"], state_data["field"], new_value
        )
        await state.clear()

    async def _send_success_message(
        self, message: Message, service_title: str, field: str, new_value: str
    ):
        await message.answer(
            text=ServiceMessage.success_edit(service_title, field, new_value)
        )

    async def _send_fail_message(self, message: Message):
        await message.answer(text=ServiceMessage.fail_edit())

    async def _build_keyboard(self):
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="...")  # TODO: Add actual fields

    async def _edit_service(
        self, message: Message, service_id: int, field: str, new_value: str
    ) -> ResultDTO:
        result = await self._edit_service_uc(service_id, **{field: new_value})
        if result.is_success:
            await self._send_success_message(
                message, result.data.title, field, new_value
            )
        else:
            await self._send_fail_message(message)


class DeactivateServiceHandler:
    def __init__(self, container: Container):
        self._get_service_us: GetServicesUseCase = container.resolve(GetServicesUseCase)
        self._edit_service_uc: EditServiceUseCase = container.resolve(
            EditServiceUseCase
        )

    async def show_service(self, message: Message, state: FSMContext):
        result = await self._get_service_us()
        keyboard = DisplayData.create_button(result.data, ("data",), ("id",))
        await state.set_state(DeleteServiceStates.service_id)
        await message.answer(text=ServiceMessage.deactivate(), reply_markup=keyboard)

    async def handle_set_selected_service(
        self, callback: CallbackQuery, state: FSMContext
    ):
        service_id = await callback.data
        result = await self._edit_service_uc(service_id, is_active=False)
        if result.is_success:
            await callback.message.answer(
                text=ServiceMessage.success_deactivate(result.data.title)
            )
        else:
            await callback.message.answer(text=ServiceMessage.fail_deactivate())
        await state.clear()
