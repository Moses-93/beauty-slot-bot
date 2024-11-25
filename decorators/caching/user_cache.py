import logging
from cache.cache import user_cache, request_cache
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


def cache_username(func):
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        name = event.from_user.first_name
        username = event.from_user.username
        user_id = event.from_user.id
        logger.info(f"User ID: {user_id}, Username: {username}")

        await user_cache.set_user_cache(user_id, name=name, username=username)
        return await func(event, *args, **kwargs)

    return wrapper


def cache_date(func):
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        logger.info("Запуск декоратора для кешування дати")
        user_id = callback.from_user.id
        date_id = int(callback.data.split("_")[2])

        dates = await request_cache.get_request(key="dates")
        if dates is None:
            return await func(callback, *args, **kwargs)
        for date in dates:
            if date.id == date_id:
                await user_cache.set_user_cache(user_id, date=date)
                logger.info(f"Користувач обрав дату: {date.date}")
                break
        else:
            logger.info(f"No date found for ID: {date_id}")

        return await func(callback, *args, **kwargs)

    return wrapper


def cache_service(func):
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        logger.info("Запуск декоратора для кешування послуги")

        user_id = callback.from_user.id
        service_id = int(callback.data.split("_")[2])

        services = await request_cache.get_request(key="services")
        if services is None:
            return await func(callback, *args, **kwargs)
        for service in services:
            if service.id == service_id:
                await user_cache.set_user_cache(user_id, service=service)
                logger.info(f"Користувач обрав послугу: {service.name}")
                break
        else:
            logger.info(f"No service found for ID: {service_id}")

        return await func(callback, *args, **kwargs)

    return wrapper


def cache_note_id(func):
    async def wrapper(*args, **kwargs):
        note = await func(*args, **kwargs)
        if note:
            user_id = note.user_id
            await user_cache.set_user_cache(user_id, note_id=note.id)
        return note

    return wrapper
