import logging

from aiogram import F, Router
from aiogram.types import Message

from ..middleware import AdminMiddleware
from ..keyboards import (
    date_keyboard,
    general_keyboards,
    service_keybord,
    show_booking_keyboards,
)
from decorators.permissions import admin_only

logger = logging.getLogger(__name__)

router = Router()
router.message.middleware(AdminMiddleware())
router.callback_query.middleware(AdminMiddleware())


@router.message(F.text == "admin")
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


@router.message(F.text == "Керування послугами")
@admin_only
async def manage_services(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    keyboard = service_keybord.manage_service_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
    return


@router.message(F.text == "Керування датами")
@admin_only
async def manage_dates(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    keyboard = date_keyboard.manage_dates_keyboard
    await message.answer(text=msg, reply_markup=keyboard)


@router.message(F.text == "Керування адміністраторами")
@admin_only
async def manage_admins(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    keyboard = general_keyboards.manage_admins_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
    return


@router.message(F.text == "Записи")
@admin_only
async def show_all_bookings(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    keyboard = show_booking_keyboards.show_bookings_keyboard
    await message.answer(text=msg, reply_markup=keyboard)
