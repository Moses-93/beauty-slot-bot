from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Управління послугами"),
            KeyboardButton(text="Управління датами"),
            KeyboardButton(text="Записи"),
        ]
    ],
    resize_keyboard=True,
)
