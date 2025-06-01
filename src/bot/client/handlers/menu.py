import logging
from punq import Container
from aiogram.types import Message


logger = logging.getLogger(__name__)


class MenuHandler:
    def __init__(self, container: Container):
        self._container = container

    async def make_appointment(message: Message): ...
