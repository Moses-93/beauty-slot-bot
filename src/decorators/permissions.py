from aiogram.types import Message


def admin_only(func):
    async def wrapper(event: Message, *args, **kwargs):
        if kwargs.get("is_admin"):
            return await func(event, *args, **kwargs)
        else:
            await event.answer(text="У вас немає доступу до цієї функції.")
            return

    return wrapper
