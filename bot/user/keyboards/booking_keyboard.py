from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from db.db_reader import GetFreeDate, GetService


async def services_keyboard(act):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=service.name, callback_data=f"{act}_service_{int(service.id)}"
                )
            ]
            for service in await GetService(all_services=True).get()
        ]
    )


async def free_dates_keyboard(act):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=str(free_date.date), callback_data=f"{act}_date_{int(free_date.id)}"
                )
            ]
            for free_date in await GetFreeDate(free_dates=True).get()
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


notes = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Всі записи", callback_data="all_notes")],
        [InlineKeyboardButton(text="Активні записи", callback_data="active_notes")],
    ]
)
