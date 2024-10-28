from aiogram import F, Router
from aiogram.types import Message
from ..keyboards.admin_keyboards import (
    main_keyboard,
    manage_service_keyboard,
    manage_dates_keyboard,
    show_bookings_keyboard,
)
import logging
from decorators.check_user import only_admin

admin_router = Router()

logger = logging.getLogger(__name__)


@admin_router.message(F.text == "admin")
async def show_admin_panel(message: Message, is_admin: bool, *args, **kwargs):
    logger.info(f"USER ID(show_admin_panel): {is_admin}")
    if is_admin:
        await message.answer(
            text="Ви перейшли в панель адміністратора", reply_markup=main_keyboard
        )
        return
    else:
        await message.answer(text="У Вас немає доступу до адмін панелі.")
        return


@admin_router.message(F.text == "Управління послугами")
@only_admin
async def manage_services(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    await message.answer(text=msg, reply_markup=manage_service_keyboard)
    return


@admin_router.message(F.text == "Управління датами")
@only_admin
async def manage_dates(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    await message.answer(text=msg, reply_markup=manage_dates_keyboard)


@admin_router.message(F.text == "Записи")
@only_admin
async def show_all_bookings(message: Message, *args, **kwargs):
    msg = "Оберіть дію:"
    await message.answer(text=msg, reply_markup=show_bookings_keyboard)
