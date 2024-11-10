from aiogram.types import CallbackQuery
from db.db_reader import GetNotes
from bot.admin.keyboards.date_keyboard import delete_date_keyboard
from bot.admin.keyboards.service_keybord import delete_service_keyboard
from utils.message_templates import template_manager


def prevent_deletion_if_related(date: bool = False, service: bool = False):
    def decorator(func):
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            if date:
                date_id = int(callback.data.split("_")[2])
                notes = await GetNotes(date_id=date_id).get_notes()
                if notes:
                    user_ids = []
                    for note in notes:
                        user_ids.append(note.user_id)
                    msg = template_manager.get_warning_del_date_or_service(date=True)
                    keyboard = delete_date_keyboard(date_id, user_ids)
                    await callback.message.answer(text=msg, reply_markup=keyboard)
                    await callback.answer()
                    return
            elif service:
                user_id = callback.from_user.id
                service_id = int(callback.data.split("_")[2])

                notes = await GetNotes(user_id=user_id, only_active=True).get_notes()
                for note in notes:
                    user_ids = []
                    if note.service_id == service_id:
                        user_ids.append(note.user_id)
                        msg = template_manager.get_warning_del_date_or_service()
                        keyboard = delete_service_keyboard(user_ids, service_id)
                        await callback.message.answer(text=msg, reply_markup=keyboard)
                        await callback.answer()
                        return
            return await func(callback, *args, **kwargs)

        return wrapper

    return decorator
