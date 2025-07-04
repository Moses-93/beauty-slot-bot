import logging
from punq import Container
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.master.states.time_slot import CreateTimeSlotStates, CancelTimeSlotStates


logger = logging.getLogger(__name__)


class CreateTimeSlotHandler:
    def __init__(self, container: Container):
        self._container = container

    async def handle_start_add_date(self, message: Message, state: FSMContext):
        await state.set_state(CreateTimeSlotStates.date)
        await message.answer(text=...)

    async def handle_set_date(self, message: Message, state: FSMContext, date: str):
        await state.set_state(CreateTimeSlotStates.start_time)
        await state.update_data(date=date)
        await message.answer(text=...)

    async def handle_set_deactivation_time(
        self, message: Message, state: FSMContext, deactivation_time: str
    ):
        await state.update_data(deactivation_time=deactivation_time)

    async def _add_date(self, date: str, deactivation_time: str):
        pass


class CancelTimeSlotHandler:
    def __init__(self, container: Container):
        self._container = container

    async def handle_start_deactivate_date(self, message: Message, state: FSMContext):
        await state.set_state(CancelTimeSlotStates.time_slot_id)
        await message.answer(text=..., reply_markup=...)

    async def handle_delete_date(self, callback: CallbackQuery, state: FSMContext):
        pass

    async def _deactivate_date(self, date_id: int):
        pass
