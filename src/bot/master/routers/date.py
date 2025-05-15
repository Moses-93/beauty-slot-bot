from aiogram import Router, F
from punq import Container

from src.bot.master.states.date import CreateDateStates, DeleteDateStates
from src.bot.master.handlers.date import DateHandler


class DateRouter:
    def __init__(self, container: Container):
        self._container = container
        self.router = Router()
        self.handler = DateHandler(container)
        self.register()

    def register(self):
        self.router.message(F.text == "📅 Дати")(self.handler.show_dates_menu)
        self.router.message(F.text == "➕ Додати дату")(
            self.handler.handle_start_add_date
        )
        self.router.message(F.text == "➖ Видалити дату")(
            self.handler.handle_start_delete_date
        )
        self.router.message(F.text == "📋 Список дат")(self.handler.show_dates_list)
        self.router.message(CreateDateStates.date, self.handler.handle_set_date)
        self.router.message(
            CreateDateStates.deactivation_time,
            self.handler.handle_set_deactivation_time,
        )
        self.router.callback_query(
            DeleteDateStates.date_id, self.handler.handle_delete_date
        )
