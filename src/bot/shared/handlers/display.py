import logging
from punq import Container
from aiogram.types import Message, CallbackQuery


logger = logging.getLogger(__name__)


class DisplayHandler:
    def __init__(self, container: Container):
        self._container = container

    async def show_all_bookings(self, callback: CallbackQuery): ...

    async def show_active_bookings(self, callback: CallbackQuery): ...

    async def show_services(self, message: Message): ...

    async def show_dates(self, message: Message): ...

    async def show_contacts(self, message: Message): ...


class CommandStartHandler:
    def __init__(self, container: Container):
        self._container = container

    async def start(message: Message): ...
