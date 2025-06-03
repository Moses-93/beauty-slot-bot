from aiogram import Router, F
from aiogram.filters import CommandStart

from src.bot.master.handlers.navigation import SectionHandler


class SectionRouter:
    def __init__(self, handler: SectionHandler):
        self._router = Router(name="section")
        self._handler = handler
        self._register()

    @property
    def router(self):
        return self._router

    def _register(self) -> None:
        self._router.message.register(self._handler.show_sections, CommandStart)
        self._router.message.register(
            self._handler.show_dates_section, F.text == "📅 Дати"
        )
        self._router.message.register(
            self._handler.show_services_section, F.text == "📖 Послуги"
        )
        self._router.message.register(
            self._handler.show_booking_section, F.text == "📒 Записи"
        )
