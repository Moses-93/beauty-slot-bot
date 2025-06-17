from aiogram import F, Router
from punq import Container

from src.bot.shared.handlers.contact import ContactDisplayHandler


class ContactDisplayRouter:
    def __init__(self, container: Container):
        self._container = container
        self._router = Router()
        self._handler = ContactDisplayHandler(self._container)

    def register(self):
        self._router.message.register(
            self._handler.show_contact,
            F.text.in_(["📕 Контакти", "📕 Мої контакти"]),
        )

    @property
    def router(self) -> Router:
        return self._router
