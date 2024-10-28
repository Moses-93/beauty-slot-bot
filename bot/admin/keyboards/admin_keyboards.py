from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
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


manage_dates_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Доступні дати", callback_data="available_dates")],
        [InlineKeyboardButton(text="Додати дату", callback_data="add_date")],
        [InlineKeyboardButton(text="Видалити дату", callback_data="delete_date")],
    ]
)

manage_service_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Показати послуги", callback_data="show_services")],
        [InlineKeyboardButton(text="Додати послугу", callback_data="add_service")],
        [InlineKeyboardButton(text="Видалити послугу", callback_data="delete_service")],
        [
            InlineKeyboardButton(
                text="Редагувати послугу", callback_data="edit_services"
            )
        ],
    ],
)

show_bookings_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Всі записи", callback_data="all_notes")],
        [InlineKeyboardButton(text="Активні записи", callback_data="active_booking")],
    ]
)
