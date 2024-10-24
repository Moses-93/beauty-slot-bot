import asyncio
from aiogram import Bot
from os import getenv


class MessageSendingManager:
    def __init__(self, token: str):
        self.bot = Bot(token=token)

    async def send_message(self, chat_id: int, message: str):
        await self.bot.send_message(chat_id=chat_id, text=message)

    # def send(self, chat_id: int, message: str):
    #     """Зручний метод для асинхронного виклику у синхронному коді."""
    #     loop = asyncio.get_event_loop()
    #     if loop.is_running():
    #         # Якщо цикл вже працює, використовуємо інший підхід
    #         asyncio.create_task(self.send_message(chat_id, message))
    #     else:
    #         # Якщо цикл не запущений, запускаємо асинхронно
    #         loop.run_until_complete(self.send_message(chat_id, message))


# Ініціалізація менеджера
TOKEN = getenv("SENDERS_TOKEN")
manager = MessageSendingManager(token=TOKEN)
