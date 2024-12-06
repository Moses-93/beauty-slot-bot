from aiogram import F, Router
from aiogram.types import Message
from ..keyboards import (
    date_keyboard,
    general_keyboards,
    service_keybord,
    show_booking_keyboards,
)
import logging
from decorators.check.check_user import only_admin

admin_router = Router()

logger = logging.getLogger(__name__)


@admin_router.message(F.text == "admin")
async def show_admin_panel(message: Message, is_admin: bool, *args, **kwargs):
    logger.info(f"USER ID(show_admin_panel): {is_admin}")
    if is_admin:
        msg = "Ви перейшли в панель адміністратора"
        keyboard = general_keyboards.main_keyboard
        await message.answer(text=msg, reply_markup=keyboard)
        return
    else:
        await message.answer(text="У Вас немає доступу до адмін панелі.")
        return


@admin_router.message(F.text == "Керування послугами")
@only_admin
async def manage_services(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    keyboard = service_keybord.manage_service_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
    return


@admin_router.message(F.text == "Керування датами")
@only_admin
async def manage_dates(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    keyboard = date_keyboard.manage_dates_keyboard
    await message.answer(text=msg, reply_markup=keyboard)


@admin_router.message(F.text == "Керування адміністраторами")
@only_admin
async def manage_admins(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    keyboard = general_keyboards.manage_admins_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
    return


@admin_router.message(F.text == "Записи")
@only_admin
async def show_all_bookings(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    keyboard = show_booking_keyboards.show_bookings_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
