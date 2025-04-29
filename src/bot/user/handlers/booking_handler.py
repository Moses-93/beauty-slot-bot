import logging

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from datetime import datetime

from src.bot.user.keyboards.booking_keyboard import free_dates_keyboard
from src.bot.user.keyboards.reminder_keyboard import reminder_button

from src.decorators.validation import require_field
from src.decorators.cache_tools import user_caching
from src.utils.message_templates import template_manager
from src.utils.utils import handlers_time, promote_booking

from src.db.crud import dates_manager, services_manager
from src.db.models import Dates

from src.cache.cache import user_cache


time_pattern = r"^(1[0-7]:[0-5]\d|18:00)$"

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(lambda c: c.data.startswith("service_"))
@user_caching(key="service", fetch_from_db=lambda id: services_manager.read(id=id))
async def processes_services(callback: CallbackQuery, *args, **kwargs):
    logger.info("Запуск обробника послуг")
    dates = await dates_manager.read(free=True)
    if not dates:
        msg = "На жаль доступних дат немає"
        await callback.message.answer(text=msg)
        return await callback.answer()
    msg = template_manager.service_selection_info()
    keyboard = await free_dates_keyboard(act="date", free_dates=dates)
    await callback.message.answer(
        text=msg,
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("date_date_"))
@user_caching(key="date", fetch_from_db=lambda id: dates_manager.read(id=id))
@require_field(fields=["service"])
async def processes_dates(callback: CallbackQuery, *args, **kwargs):
    logger.info("Запуск обробника дат")
    msg = template_manager.date_selection_prompt()
    await callback.message.answer(text=msg)
    await callback.answer()


@router.message(F.text.regexp(time_pattern))
@require_field(fields=["date", "service"])
async def processes_time(message: Message, user_id, *args, **kwars):
    logger.info("Запуск обробника часу")
    time = message.text
    logger.info(f"User selected time(processes_time): {time}")
    handlers = await handlers_time(user_id, time)
    if handlers is None:  # Користувач успішно записався
        msg = await template_manager.successful_booking_notification(user_id, time)
        await message.answer(text=msg, reply_markup=reminder_button)
    elif handlers[0] == False:  # Користувач обрав минулий час
        _, msg = handlers
        await message.answer(text=msg)
    else:  # Користувач обрав час у зайнятому діапазоні, повернулась пропозиція з часом
        message_text, keyboard = handlers
        await message.answer(text=message_text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_the_entry(callback: CallbackQuery, user_id):
    logger.info("Запуск обробника підтвердження запропонованого часу")
    time = callback.data.split("_")[-1]
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    logger.info(f"Time selected(in confirm_the_entry): {time} | type: {type(time)}")
    try:
        await promote_booking(user_id=user_id, time=time)
    except TypeError:
        logger.error("Помилка під час підтвердження запропонованого часу")
        await callback.message.answer(
            text="Виникла помилка під час запису.\nСпробуйте записатись ще раз"
        )
        await callback.answer()
        return
    except AttributeError:
        logger.error(f"Користувач натиснув на кнопку підтвердження ще раз")
        await callback.message.answer(text="Запис вже було підтверджено")
        await callback.answer()
        return

    msg = await template_manager.successful_booking_notification(user_id, time.time())
    await user_cache.clear_user_cache(user_id, "note_id")
    await callback.message.answer(text=msg, reply_markup=reminder_button)
    await callback.answer()
