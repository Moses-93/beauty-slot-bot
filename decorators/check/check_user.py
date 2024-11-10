from aiogram.types import Message, CallbackQuery


def only_admin(func):
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs):
        if kwargs.get("is_admin"):
            return await func(event, *args, **kwargs)
        else:
            await event.answer(text="У вас немає доступу до цієї функції.")
            return

    return wrapper
