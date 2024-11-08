from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)


show_periods = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"{day}", callback_data=f"days_{day}")]
        for day in [1, 3, 7, 15, 30]
    ]
)

show_bookings_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Фільтрувати записи")],
        [KeyboardButton(text="Всі активні записи")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)
