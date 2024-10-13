from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from utils.db import free_dates, services


keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Послуги")], [KeyboardButton(text="Записатись")]],
    resize_keyboard=True,
)


services_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=str(service), callback_data=f"service_{service.id}")]
        for service in services
    ]
)


free_dates_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=str(free_date.date), callback_data=f"date_{free_date.id}"
            )
        ]
        for free_date in free_dates
    ]
)


def confirm_time_keyboard(time):
    confirm = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Підтвердити {time}", callback_data=f"confirm_{time}"
                )
            ]
        ]
    )
    return confirm
