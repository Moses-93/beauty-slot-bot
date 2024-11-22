import logging
from aiogram.types import Message, CallbackQuery
from db.db_reader import GetFreeDate, GetService
from cache.cache import request_cache
from decorators.check.deletion_checks import PreventDeletionError

logger = logging.getLogger(__name__)


def get_free_dates(func):
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        logger.info("Виклик декоратора для отримання вільних дат")
        dates = await request_cache.get_request(key="free_dates")
        if not dates:
            logger.info("Відбувся запит в БД для отримання вільних дат")
            dates = await GetFreeDate(free_dates=True).get()
            logger.info(f"Отримано: {dates}")
            await request_cache.set_request(key="free_dates", value=dates)
        return await func(event, dates, *args, **kwargs)

    return wrapper


def get_service(func):
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        logger.info("Виклик декоратора для отримання послуг")
        services = await request_cache.get_request(key="services")
        if not services:
            logger.info("Відбувся запит в БД для отримання послуг")
            services = await GetService(all_services=True).get()
            await request_cache.set_request(key="services", value=services)
        return await func(event, services, *args, **kwargs)

    return wrapper


def update_cache(date=False, service=False):
    def decorator(func):
        async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
            await func(event, *args, **kwargs)
            if date:
                logger.info("Оновлення кеша вільних дат")
                dates = await GetFreeDate(free_dates=True).get()
                await request_cache.set_request(key="free_dates", value=dates)
                return

            if service:
                logger.info("Оновлення кеша послуг")
                services = await GetService(all_services=True).get()
                await request_cache.set_request(key="services", value=services)
                return

        return wrapper

    return decorator


def clear_cache(date=False, service=False):
    def decorator(func):
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            logger.info("Запуск декоратора для очищення кеша")
            try:
                await func(callback, *args, **kwargs)
            except PreventDeletionError:
                return
            if date:
                logger.info("Очищення кеша вільних дат")
                date_id = int(callback.data.split("_")[2])
                dates = await request_cache.get_request("free_dates")
                free_date = [date for date in dates if date.id != date_id]
                await request_cache.set_request(key="free_dates", value=free_date)
                return

            elif service:
                logger.info("Очищення кеша послуг")
                service_id = int(callback.data.split("_")[2])
                services = await request_cache.get_request("services")
                services = [service for service in services if service.id != service_id]
                await request_cache.set_request(key="services", value=services)
                return

        return wrapper

    return decorator
