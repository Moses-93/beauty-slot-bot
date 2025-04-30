from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cancel_booking_button(active_notes):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Скасувати запис - {note.id}",
                    callback_data=f"note_{note.id}_{note.name}_{note.date}_{note.time}",
                )
            ]
            for note in active_notes
        ]
    )
    return keyboard
