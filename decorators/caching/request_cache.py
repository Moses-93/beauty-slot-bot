import logging
from aiogram.types import Message, CallbackQuery
from db.db_reader import get_date, get_service
from cache.cache import request_cache

logger = logging.getLogger(__name__)


def get_free_dates(func):
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        logger.info("Запуск декоратора для отримання вільних дат")
        dates = await request_cache.get_request(key="dates")
        if not dates:
            logger.info("Відбувся запит в БД для отримання вільних дат")
            dates = await get_date.get_date(free=True)
            logger.info(f"Отримано: {dates}")
            await request_cache.set_request(key="dates", value=dates)
        return await func(event, dates, *args, **kwargs)

    return wrapper


def get_all_service(func):
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        logger.info("Запуск декоратора для отримання послуг")
        services = await request_cache.get_request(key="services")
        if not services:
            logger.info("Відбувся запит в БД для отримання послуг")
            services = await get_service.get_service()
            await request_cache.set_request(key="services", value=services)
        return await func(event, services, *args, **kwargs)

    return wrapper


def update_cache(key: str):
    def decorator(func):
        async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
            logger.info("Запуск декоратора для оновлення кеша")
            result = await func(event, *args, **kwargs)
            if result is None:
                return
            if key == "dates":
                logger.info("Оновлення кеша вільних дат")
                data = await get_date.get_date(free=True)
            if key == "services":
                logger.info("Оновлення кеша послуг")
                data = await get_service.get_service()

            await request_cache.set_request(key=key, value=data)
            return True

        return wrapper

    return decorator


def clear_cache(key: str):
    def decorator(func):
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            logger.info("Запуск декоратора для очищення кеша")
            result = await func(callback, *args, **kwargs)
            if result is None:
                return
            value_id = int(callback.data.split("_")[2])
            query = await request_cache.get_request(key=key)
            if not query:
                return
            logger.info(f"Очищення кеша для {key}")
            new_cache = [item for item in query if item.id != value_id]

            await request_cache.set_request(key=key, value=new_cache)

        return wrapper

    return decorator
