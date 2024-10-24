from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)
from db.db_reader import GetFreeDate, GetService

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

notes = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Всі записи", callback_data="all_notes")],
        [InlineKeyboardButton(text="Активні записи", callback_data="active_notes")],
    ]
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


reminder_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Нагадати про запис", callback_data="show_reminder")]
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


def cancel_the_notes(active_notes):
    cancel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Скасувати запис на {str(note.free_date.date)} {note.time}",
                    callback_data=f"note_{note.id}",
                )
            ]
            for note in active_notes
        ]
    )
    return cancel


def create_reminder_keyboards():
    hours = [1, 2, 4, 6]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f" За {hour} год.", callback_data=f"reminder_{hour}"
                )
                for hour in hours
            ]
        ]
    )
    return keyboard
