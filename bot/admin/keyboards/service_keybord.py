from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)

manage_service_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Показати послуги")],
        [KeyboardButton(text="Додати послугу")],
        [KeyboardButton(text="Видалити послугу")],
        [KeyboardButton(text="Редагувати послугу")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)

edit_service_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назва", callback_data="field_name")],
        [InlineKeyboardButton(text="Вартість", callback_data="field_price")],
        [InlineKeyboardButton(text="Тривалість", callback_data="field_durations")],
    ]
)


def delete_service_keyboard(user_ids: list[int], service_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Продовжити видалення",
                    callback_data=f"del_service_{user_ids}_{service_id}",
                )
            ],
        ]
    )
