import logging

from aiogram.types import CallbackQuery

from src.cache.config import caches
from src.cache.cache import user_cache


logger = logging.getLogger(__name__)


def user_caching(key: str, fetch_from_db):
    def decorator(func):
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            logger.info(f"Запуск декоратора для кешування за ключем: {key}")
            user_id = callback.from_user.id
            username = callback.from_user.username
            name = callback.from_user.first_name
            id = int(callback.data.split("_")[2])
            *_, result = await fetch_from_db(id=id)
            if result:
                logger.info(f"Result: {result} | type: {type(result)}")
                await user_cache.set_user_cache(
                    user_id=user_id, **{key: result, "name": name, "username": username}
                )
            return await func(callback, *args, **kwargs)

        return wrapper

    return decorator


def cache_note_id(func):
    async def wrapper(*args, **kwargs):
        logger.info("Запуск декоратора для кешування замовлення за ID")
        note = await func(*args, **kwargs)
        logger.info(f"Note: {note} | type: {type(note)}")
        if note:
            await user_cache.set_user_cache(user_id=note.user_id, note_id=note.id)
        return note

    return wrapper


def clear_cache(func):
    async def wrapper(*args, **kwargs):
        logger.info("Запуск декоратора для очищення кешу")
        result = await func(*args, **kwargs)
        logger.info(f"Result: {result} | type: {type(result)}")
        if result:
            await caches.get(alias="queries_cache").clear()
            return result

    return wrapper
