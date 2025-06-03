import logging
from punq import Container
from aiogram.types import Message


logger = logging.getLogger(__name__)


class MenuHandler:
    def __init__(self, container: Container):
        self._container = container

    async def show_booking(message: Message): ...

    async def show_services(message: Message): ...

    async def show_dates(message: Message): ...

    async def show_contacts(message: Message): ...


class CommandStartHandler:
    def __init__(self, container: Container):
        self._container = container

    async def start(message: Message): ...
