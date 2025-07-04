import logging
from punq import Container
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.master.states.time_slot import CreateTimeSlotStates, CancelTimeSlotStates


logger = logging.getLogger(__name__)


class CreateTimeSlotHandler:
    def __init__(self, container: Container):
        self._container = container

    async def handle_add_time_slot(self, message: Message, state: FSMContext):
        await state.set_state(CreateTimeSlotStates.date)
        await message.answer(
            text=...
        )  # TODO: Add a message prompting the user to set a date

    async def handle_set_date(self, message: Message, state: FSMContext, date: str):
        await state.set_state(CreateTimeSlotStates.start_time)
        await state.update_data(date=date)
        await message.answer(
            text=...
        )  # TODO: Add a message prompting the user to set a start time

    async def handle_set_start_time(
        self, message: Message, state: FSMContext, start_time: str
    ):
        await state.set_state(CreateTimeSlotStates.end_time)
        await state.update_data(start_time=start_time)
        await message.answer(
            text=...
        )  # TODO: Add a message prompting the user to set an end time

    async def handle_set_end_time(
        self, message: Message, state: FSMContext, end_time: str
    ):
        await state.update_data(end_time=end_time)


class CancelTimeSlotHandler:
    def __init__(self, container: Container):
        self._container = container

    async def handle_start_cancel_time_slot(self, message: Message, state: FSMContext):
        await state.set_state(CancelTimeSlotStates.time_slot_id)
        await message.answer(
            text=..., reply_markup=...
        )  # TODO Add a message prompting the user to select a time slot to cancel

    async def handle_cancel_time_slot(self, callback: CallbackQuery, state: FSMContext):
        pass
