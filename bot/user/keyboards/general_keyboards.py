from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записатись")],
        [KeyboardButton(text="Мої записи")],
        [KeyboardButton(text="Послуги")],
        [KeyboardButton(text="Контакти")],
    ],
    resize_keyboard=True,
)
