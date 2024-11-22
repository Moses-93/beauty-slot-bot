from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

manage_dates_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Доступні дати")],
        [KeyboardButton(text="Додати дату")],
        [KeyboardButton(text="Видалити дату")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)


def delete_date_keyboard(date_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Продовжити видалення",
                    callback_data=f"del_date_{date_id}",
                )
            ],
        ],
    )
