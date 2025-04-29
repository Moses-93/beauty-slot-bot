import logging
from aiogram import Bot
from os import getenv

logger = logging.getLogger(__name__)


class MessageSendingManager:
    def __init__(self, token: str, backup_token: str = None):
        self.bot = Bot(token=token)
        self.backup_bot = Bot(token=backup_token) if backup_token else None

    async def send_message(self, chat_id: int, message: str):
        """
        Використовується aiogram для відправки повідомлення в чат
        """
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
            logger.info(f"Повідомлення відправлено для користувача: {chat_id}")
        except Exception:
            logger.error(
                f"Помилка відправлення повідомлення для користувача: {chat_id}"
            )
            await self.backup_bot.send_message(chat_id=chat_id, text=message)
            logger.warning(f"Повідомлення відправленно основним ботом")


# Ініціалізація менеджера
TOKEN = getenv("SENDERS_TOKEN")
BACKUP_TOKEN = getenv("TOKEN")
manager = MessageSendingManager(token=TOKEN, backup_token=BACKUP_TOKEN)
