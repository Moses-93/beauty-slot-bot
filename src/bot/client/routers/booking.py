from aiogram import F, Router
from punq import Container

from src.bot.client.states.booking import BookingStates
from src.bot.client.handlers.booking_handler import BookingHandler


class BookingRouter:
    def __init__(self, container: Container):
        self._container = container
        self.router = Router()
        self.handler = BookingHandler(container)
        self.register_routes()

    def register_routes(self):
        self.router.message(self.handler.start)
        self.router.callback_query(BookingStates.service, self.handler.handle_service)
        self.router.callback_query(BookingStates.date, self.handler.handle_date)
        self.router.message(BookingStates.time, self.handler.handle_time)
        self.router.message(BookingStates.reminder, self.handler.handle_reminder)
        self.router.callback_query(BookingStates.confirm, self.handler.handle_confirm)
