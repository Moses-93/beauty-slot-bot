from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from utils.db import free_dates


keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Послуги")], [KeyboardButton(text="Записатись")]],
    resize_keyboard=True,
)


services_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Корекція", callback_data="correction")],
        [InlineKeyboardButton(text="Фарбування", callback_data="coloring")],
        [InlineKeyboardButton(text="Корекція+Фарбування", callback_data="correction_coloring")]
    ]
)


free_dates_list = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=str(free_date), callback_data=f"service_{free_date.id}")]
        for free_date in free_dates])
