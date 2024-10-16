from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from db.commands import GetFreeDate, GetService

free_dates = GetFreeDate().get_all_free_dates()
services = GetService().get_all_services()


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Записатись")],
        [KeyboardButton(text="Мої записи")],
        [KeyboardButton(text="Послуги")],
        [KeyboardButton(text="Контакти")],
    ],
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
