import logging
from aiogram import Bot
from os import getenv

logger = logging.getLogger(__name__)


class MessageSendingManager:
    def __init__(self, token: str):
        self.bot = Bot(token=token)

    async def send_message(self, chat_id: int, message: str):
        """
        Використовується aiogram для відправки повідомлення в чат
        """
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
        except Exception:
            logger.error(
                f"Помилка відправлення повідомлення для користувача: {chat_id}"
            )


# Ініціалізація менеджера
TOKEN = getenv("SENDERS_TOKEN")
manager = MessageSendingManager(token=TOKEN)
