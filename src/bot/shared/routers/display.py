from aiogram import Router, F

from src.bot.shared.handlers.display import DisplayHandler


class DisplayRouter:
    def __init__(self, display_handler: DisplayHandler):
        self._router = Router(name="display_router")
        self._display_handler = display_handler
        self._register()

    def _register(self):
        pass
