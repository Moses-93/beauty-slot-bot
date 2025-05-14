from aiogram import Router, F
from punq import Container

from src.bot.client.handlers.menu import MenuHandler


class MenuRouter:
    def __init__(self, container: Container):
        self._container = container
        self.handler = MenuHandler(container)
        self.router = Router()
        self.register()

    def register(self):
        self.router.message(F.text == "📝 Записатися", self.handler.make_appointment)
        self.router.message(F.text == "📖 Мої записи")(self.handler.show_booking)
        self.router.message(F.text == "📋 Послуги")(self.handler.show_services)
        self.router.message(F.text == "🗓 Доступні дати")(self.handler.show_dates)
        self.router.message(F.text == "📕 Контакти")(self.handler.show_contacts)
