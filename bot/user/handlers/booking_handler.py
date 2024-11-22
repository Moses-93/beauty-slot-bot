from datetime import datetime
from aiogram.types import Message, CallbackQuery
import logging
from bot.user.keyboards.booking_keyboard import free_dates_keyboard
from decorators.caching.request_cache import get_free_dates, get_service
from decorators.validators.data_validation_in_user_data import check_user_data
from cache.cache import user_cache
from decorators.caching.user_cache import cache_username, cache_date, cache_service
from utils.message_templates import template_manager
from utils.utils import handlers_time, promote_booking
from bot.user.keyboards.reminder_keyboard import reminder_button
from aiogram import F, Router

time_pattern = r"^(1[0-7]:[0-5]\d|18:00)$"
logger = logging.getLogger(__name__)
booking_router = Router()


@booking_router.callback_query(lambda c: c.data.startswith("service_"))
@cache_service
@cache_username
@get_free_dates
async def processes_services(callback: CallbackQuery, dates, *args, **kwargs):
    logger.info("Запуск обробника послуг")
    msg = template_manager.service_selection_info()
    keyboard = await free_dates_keyboard(act="date", free_dates=dates)
    await callback.message.answer(
        text=msg,
        reply_markup=keyboard,
    )
    await callback.answer()


@booking_router.callback_query(lambda c: c.data.startswith("date_date_"))
@cache_date
@check_user_data(["service"])
async def processes_dates(callback: CallbackQuery, *args, **kwargs):
    logger.info("Запуск обробника дат")
    msg = template_manager.date_selection_prompt()
    await callback.message.answer(text=msg)
    await callback.answer()


@booking_router.message(F.text.regexp(time_pattern))
@check_user_data(["date", "service"])
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


@booking_router.callback_query(lambda c: c.data.startswith("confirm_"))
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
