import os
import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.user.handlers import (
    general_handlers,
    booking_handler,
    cancellation_handlers,
    reminder_handlers,
    show_booking,
)
from bot.admin.handlers import (
    general_handlers as admin_hndlrs,
    service_handlers,
    dates_handlers,
    show_bookings,
    admins_handlers,
)
from bot.user.middleware import UserIDMiddleware

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
dp.message.middleware(UserIDMiddleware())
dp.callback_query.middleware(UserIDMiddleware())


async def main():
    dp.include_router(admins_handlers.router)
    dp.include_router(general_handlers.router)
    dp.include_router(show_booking.router)
    dp.include_router(cancellation_handlers.router)
    dp.include_router(reminder_handlers.router)
    dp.include_router(booking_handler.router)
    dp.include_router(admin_hndlrs.router)
    dp.include_router(service_handlers.router)
    dp.include_router(dates_handlers.router)
    dp.include_router(show_bookings.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(find_time_for_reminder, "interval", minutes=10)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
