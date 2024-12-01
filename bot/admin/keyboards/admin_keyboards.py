from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Керування послугами"),
            KeyboardButton(text="Керування датами"),
        ],
        [KeyboardButton(text="Керування адміністраторами")],
        [KeyboardButton(text="Записи")],
    ],
    resize_keyboard=True,
)

manage_admins_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Додати адміністратора"),
            KeyboardButton(text="Видалити адміністратора"),
        ],
        [KeyboardButton(text="Список адміністраторів")],
        [KeyboardButton(text="Назад")],
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
