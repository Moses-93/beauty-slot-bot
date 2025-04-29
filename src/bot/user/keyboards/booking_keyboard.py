import logging
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

logger = logging.getLogger(__name__)


async def services_keyboard(act: str, services):
    message = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=service.name, callback_data=f"{act}_service_{service.id}"
                )
            ]
            for service in services
        ]
    )
    return message


async def free_dates_keyboard(act: str, free_dates):
    message = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=str(free_date.date),
                    callback_data=f"{act}_date_{free_date.id}",
                )
            ]
            for free_date in free_dates
        ]
    )
    return message


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


notes = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Всі записи", callback_data="all_notes")],
        [InlineKeyboardButton(text="Активні записи", callback_data="active_notes")],
    ]
)
