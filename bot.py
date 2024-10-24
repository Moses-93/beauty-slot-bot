import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
import os
from bot.handlers import router
from utils.booking_reminders import find_time_for_reminder
from apscheduler.schedulers.asyncio import AsyncIOScheduler


os.environ["TZ"] = "Europe/Kyiv"

logging.basicConfig(
    level=logging.INFO,  # Рівень логування (INFO для загальної інформації)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат повідомлень
    handlers=[
        logging.FileHandler("logs/bot.log"),  # Файл для зберігання логів
        logging.StreamHandler(),  # Виведення логів у консоль
    ],
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(find_time_for_reminder, "interval", minutes=2)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
