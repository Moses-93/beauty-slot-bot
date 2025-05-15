import logging
from punq import Container
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.keyboard.master import MasterKeyboard
from src.bot.master.states.date import CreateDateStates, DeleteDateStates
from src.bot.messages.date import DateMessage


logger = logging.getLogger(__name__)


class DateHandler:
    def __init__(self, container: Container):
        self._container = container

    async def show_dates_menu(self, message: Message):
        await message.answer(
            text=DateMessage.start(),
            reply_markup=MasterKeyboard.dates_section(),
        )

    async def handle_start_add_date(message: Message, state: FSMContext):
        await state.set_state(CreateDateStates.date)
        await message.answer(text=...)

    async def handle_start_delete_date(message: Message, state: FSMContext):
        await state.set_state(DeleteDateStates.date_id)
        await message.answer(text=..., reply_markup=...)

    async def show_dates_list(message: Message): ...

    async def handle_set_date(message: Message, state: FSMContext, date: str):
        await state.set_state(CreateDateStates.deactivation_time)
        await state.update_data(date=date)
        await message.answer(text=...)

    async def handle_set_deactivation_time(
        message: Message, state: FSMContext, deactivation_time: str
    ):
        await state.update_data(deactivation_time=deactivation_time)

    async def handle_delete_date(callback: CallbackQuery, state: FSMContext):
        pass
