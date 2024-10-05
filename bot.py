import asyncio

from aiogram import Bot, Dispatcher
from os import getenv
from bot.handlers import router


TOKEN = getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
