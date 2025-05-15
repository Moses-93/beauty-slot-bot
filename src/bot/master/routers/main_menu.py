from aiogram import Router, F
from src.bot.master.handlers.menu import MenuHandler


class MenuRouter:
    def __init__(self):
        self.router = Router()
        self.handler = MenuHandler()

    def register(self):
        self.router.message(F.text == "📖 Послуги")(self.handler.show_services_menu)
        self.router.message(F.text == "📅 Дати")(self.handler.show_dates_menu)
        self.router.message(F.text == "📒 Записи")(self.handler.show_bookings_menu)
