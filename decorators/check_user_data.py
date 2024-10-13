from functools import wraps
from user_data import user_data


def check_user_id(func):
    @wraps(func)
    async def wrapper(message, *args, **kwargs):
        user_id = message.from_user.id
        # Ініціалізуємо порожній словник, якщо немає user_id в user_data
        if user_id not in user_data:
            await message.answer('Спочатку виберіть послугу та дату')
            await message.answer()

        # Перевіряємо, чи вибрав користувач послугу
        if "service" not in user_data[user_id]:
            await message.answer("Спочатку виберіть послугу.")
            return

        return await func(message, *args, **kwargs)

    return wrapper