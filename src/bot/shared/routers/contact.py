from aiogram import F, Router
from punq import Container

from src.bot.shared.handlers.contact import ContactDisplayHandler
from src.bot.shared.routers.base import BaseRouter


class ContactDisplayRouter(BaseRouter):
    def __init__(self, container: Container):
        self._handler = ContactDisplayHandler(container)
        super().__init__(Router())

    def _register(self):
        self.router.message.register(
            self._handler.show_contact,
            F.text.in_(["📕 Контакти", "📕 Мої контакти"]),
        )
