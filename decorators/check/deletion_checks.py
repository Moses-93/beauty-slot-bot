import logging
from aiogram.types import CallbackQuery
from db.db_reader import GetNotes
from bot.admin.keyboards.date_keyboard import delete_date_keyboard
from bot.admin.keyboards.service_keybord import delete_service_keyboard
from utils.message_templates import template_manager
from cache.cache import request_cache

logger = logging.getLogger(__name__)


class PreventDeletionError(Exception):
    pass


def check_booking(service: bool = False):
    def decorator(func):
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            logger.info("Запуск декоратора для перевірки бронювання")
            id = int(callback.data.split("_")[2])
            notes = await GetNotes(only_active=True).get_notes()
            user_ids = ()
            if notes:
                if service:
                    user_ids = tuple(
                        note.user_id for note in notes if note.service_id == id
                    )
                    keyboard = delete_service_keyboard(service_id=id)
                else:
                    user_ids = tuple(
                        note.user_id for note in notes if note.date_id == id
                    )
                    keyboard = delete_date_keyboard(date_id=id)
            elif user_ids:
                await request_cache.set_request(key="user_ids", value=user_ids)
                msg = template_manager.get_warning_del_date_or_service()
                await callback.message.answer(text=msg, reply_markup=keyboard)
                await callback.answer()
                raise PreventDeletionError("Існують активні записи")

            return await func(callback, id, *args, **kwargs)

        return wrapper

    return decorator
