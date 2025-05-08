from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def del_admin_button(admins: list):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{admin.id} - {admin.name}",
                    callback_data=f"del_admin_{admin.id}",
                )
            ]
            for admin in admins
        ]
    )
