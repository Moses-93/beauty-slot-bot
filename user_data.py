import logging
from cachetools import TTLCache

user_data = TTLCache(maxsize=50, ttl=1800)
logger = logging.getLogger(__name__)


def get_user_data(user_id, *args):

    if not args:
        return user_data[user_id]
    try:
        return tuple(user_data[user_id].get(key) for key in args)
    except KeyError:
        logger.error(f"Виникла помилка при доступі до даних по ключу: {user_id}")
        user_data[user_id] = {}


def set_user_data(user_id, **kwargs):

    if user_id not in user_data:
        user_data[user_id] = {}

    for key, value in kwargs.items():
        user_data[user_id][key] = value


def clean_user_data(user_id, **kwargs):
    user_data = get_user_data(user_id)  # Зміна назви на `user_data`

    keys_to_keep = set(kwargs.values())  # Створимо набір ключів, які залишаємо
    keys_to_remove = [key for key in user_data if key not in keys_to_keep]

    for key in keys_to_remove:
        user_data.pop(key)
