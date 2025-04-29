from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

reminder_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Нагадати про запис", callback_data=f"show_reminder_button"
            )
        ]
    ]
)


def create_reminder_keyboards(note_id):
    hours = [1, 2, 4, 6]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f" За {hour} год.", callback_data=f"reminder_{hour}_{note_id}"
                )
                for hour in hours
            ]
        ]
    )
    return keyboard
