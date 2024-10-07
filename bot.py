import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from os import getenv
from bot.handlers import router


logging.basicConfig(
    level=logging.INFO,  # Рівень логування (INFO для загальної інформації)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат повідомлень
    handlers=[
        logging.FileHandler("logs/bot.log"),  # Файл для зберігання логів
        logging.StreamHandler(),  # Виведення логів у консоль
    ],
)

logger = logging.getLogger(__name__)

TOKEN = getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
