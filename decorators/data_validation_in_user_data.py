from user_data import user_data
from aiogram.types import Message, CallbackQuery


def check_user_data(required_fields: list):
    def decorator(func):
        async def wrapper(event: CallbackQuery | Message, *args, **kwargs):
            user_id = event.from_user.id

            async def send_message(text: str):
                if isinstance(event, Message):
                    await event.answer(text=text)

                    return
                elif isinstance(event, CallbackQuery):
                    await event.message.answer(text=text)
                    await event.answer()
                    return

            if user_id not in user_data:
                user_data[user_id] = {}

            if not all(field in user_data[user_id] for field in required_fields):
                await send_message(text="Спочатку оберіть послугу й дату")
                return

            return await func(event, *args, **kwargs)

        return wrapper

    return decorator
