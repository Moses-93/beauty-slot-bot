from user_data import set_user_data
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cancel_booking_button(active_notes):
    for note in active_notes:
        set_user_data(note.user_id, note=note)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Скасувати запис - {note.id}",
                    callback_data=f"note_{note.id}",
                )
            ]
            for note in active_notes
        ]
    )
    return keyboard
