from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

edit_service_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назва", callback_data="field_name")],
        [InlineKeyboardButton(text="Вартість", callback_data="field_price")],
        [InlineKeyboardButton(text="Тривалість", callback_data="field_durations")],
    ]
)
