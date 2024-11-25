from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
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


async def delete_booking_keyboard(field: str, id_value: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Продовжити видалення",
                    callback_data=f"del_{field}_{id_value}",
                )
            ],
        ],
    )
