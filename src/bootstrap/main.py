import os
import asyncio

from aiogram import Bot, Dispatcher
from punq import Container

from src.core.logging import setup_logging
from src.core.config import get_settings
from src.bot.router import build_bot_router
from src.bot.middleware import setup_middlewares
from .main_container import initialize_container
from .subscriptions import register_event_subscriptions

os.environ["TZ"] = "Europe/Kyiv"
setup_logging()


async def main():
    settings = get_settings()
    bot = Bot(token=settings.telegram_token)

    container = Container()
    container.register(Bot, instance=bot)

    initialize_container(container)
    register_event_subscriptions(container)

    dp = Dispatcher()
    setup_middlewares(dp, container)
    dp.include_router(build_bot_router(container))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
