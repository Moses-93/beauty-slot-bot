from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)


show_periods = InlineKeyboardMarkup(
    inline_keyboard=[
        [   
            InlineKeyboardButton(text=f"{day}", callback_data=f"days_{day}")
        ]
        for day in [1, 3, 7, 15, 30]
    ]
)