import logging
from aiogram.types import CallbackQuery
from db.db_reader import get_notes
from bot.admin.keyboards.general_keyboards import delete_booking_keyboard
from utils.message_templates import template_manager
from cache.cache import request_cache

logger = logging.getLogger(__name__)


def check_booking(field_id: str):
    def decorator(func):
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            logger.info("Запуск декоратора для перевірки бронювання")
            id_value = int(callback.data.split("_")[2])
            notes = await get_notes.get_notes(**{field_id: id_value, "active": True})
            user_ids = ()
            if notes:
                user_ids = tuple(note.user_id for note in notes)
            if user_ids:
                keyboard = await delete_booking_keyboard(field_id, id_value)
                await request_cache.set_request(key="user_ids", value=user_ids)
                msg = template_manager.get_warning_del_date_or_service()
                await callback.message.answer(text=msg, reply_markup=keyboard)
                await callback.answer()
                return

            await func(callback, id_value, *args, **kwargs)
            return True

        return wrapper

    return decorator
