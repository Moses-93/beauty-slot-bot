import logging
from aiogram import Bot
from src.core.config import get_settings

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
            logger.info(f"Повідомлення відправлено для користувача: {chat_id}")
        except Exception:
            logger.error(
                f"Помилка відправлення повідомлення для користувача: {chat_id}"
            )


settings = get_settings()
TOKEN = settings.telegram_token
manager = MessageSendingManager(token=TOKEN)
