import os
import asyncio
from aiogram import Bot, Dispatcher

from src.core.logging import setup_logging
from src.core.config import get_settings
from src.bot.router import build_bot_router
from src.bot.middleware import setup_middlewares
from src.main_container import get_container

os.environ["TZ"] = "Europe/Kyiv"


setup_logging()


async def main():

    settings = get_settings()
    container = get_container()

    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher()

    setup_middlewares(dp, container)
    dp.include_router(build_bot_router(container))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
