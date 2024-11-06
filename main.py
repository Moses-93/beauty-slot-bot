import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
import os
from bot.user.handlers import general_handlers, booking_handler, cancellation_handlers, reminder_handlers, show_booking
from bot.admin.handlers.general_handlers import admin_router
from bot.admin.handlers.service_handlers import service_router
from bot.admin.handlers.dates_handlers import date_router
from bot.user.middleware import UserIDMiddleware
from bot.admin.middleware import AdminMiddleware
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
USER_ID_ADMIN = os.getenv("USER_ID_ADMIN")
user_ids = [1763711362, 826928022]
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.message.middleware(AdminMiddleware(user_ids))
dp.callback_query.middleware(AdminMiddleware(user_ids))
dp.message.middleware(UserIDMiddleware())
dp.callback_query.middleware(UserIDMiddleware())


async def main():
    dp.include_router(general_handlers.general_router)
    dp.include_router(show_booking.show_booking_router)
    dp.include_router(cancellation_handlers.cancellation_router)
    dp.include_router(reminder_handlers.reminder_router)
    dp.include_router(booking_handler.booking_router)
    dp.include_router(admin_router)
    dp.include_router(service_router)
    dp.include_router(date_router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(find_time_for_reminder, "interval", minutes=2)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
