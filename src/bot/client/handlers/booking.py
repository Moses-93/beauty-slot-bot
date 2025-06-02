import logging
from punq import Container
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.bot.client.states.booking import BookingStates
from application.use_cases.booking import CreateBookingUseCase
from src.application.use_cases.time_checker import CheckBookingAvailabilityUseCase
from src.bot.shared.keyboard.display_data import DisplayData
from src.bot.client.messages.booking import BookingMessage


logger = logging.getLogger(__name__)


class BookingHandler:
    def __init__(self, container: Container):
        self._container = container

    async def start(self, callback: CallbackQuery, state: FSMContext):

        await state.set_state(BookingStates.service)

    async def handle_service(
        self, callback: CallbackQuery, state: FSMContext, service_id: int
    ):
        await state.update_data(service_id=service_id)
        await state.set_state(BookingStates.date)

    async def handle_date(
        self, callback: CallbackQuery, state: FSMContext, date_id: int
    ):
        await state.update_data(date_id=date_id)
        await state.set_state(BookingStates.time)

    async def handle_time(self, message: Message, state: FSMContext, time: str):
        await state.update_data(time=time)
        await state.set_state(BookingStates.reminder)

    async def handle_reminder(
        self, message: Message, state: FSMContext, reminder_offset: int
    ): ...

    async def handle_confirm(self, callback: CallbackQuery, state: FSMContext): ...
