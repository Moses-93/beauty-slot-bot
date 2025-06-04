import logging
from punq import Container
from aiogram.types import Message, CallbackQuery


logger = logging.getLogger(__name__)


class MenuHandler:
    def __init__(self, container: Container):
        self._container = container

    async def show_all_bookings(callback: CallbackQuery): ...

    async def show_active_bookings(callback: CallbackQuery): ...

    async def show_services(message: Message): ...

    async def show_dates(message: Message): ...

    async def show_contacts(message: Message): ...


class CommandStartHandler:
    def __init__(self, container: Container):
        self._container = container

    async def start(message: Message): ...
