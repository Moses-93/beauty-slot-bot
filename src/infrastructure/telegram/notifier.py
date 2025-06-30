from aiogram import Bot

from src.application.abstractions.notifier import AbstractNotifier


class TelegramNotifier(AbstractNotifier):
    def __init__(self, bot: Bot):
        self._bot = bot

    async def send_message(self, recipient_id: str, message: str, **kwargs):
        await self._bot.send_message(
            chat_id=recipient_id, text=message, **kwargs
        )  # TODO: Add exception handling and logging
