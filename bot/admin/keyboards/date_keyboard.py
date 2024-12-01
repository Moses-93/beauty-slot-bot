from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

manage_dates_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Додати дату"), KeyboardButton(text="Видалити дату")],
        [KeyboardButton(text="Доступні дати")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)
