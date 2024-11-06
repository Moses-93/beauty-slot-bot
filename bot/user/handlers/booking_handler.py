from datetime import datetime
from aiogram.types import Message, CallbackQuery
import logging
from bot.user.keyboards.booking_keyboard import free_dates_keyboard
from decorators.data_validation_in_user_data import check_user_data
from user_data import get_user_data, set_user_data, user_data
from db.db_reader import GetFreeDate, GetService
from decorators.adding_user_data import set_username
from utils.message_templates import template_manager
from utils.utils import handlers_time, promote_booking
from bot.user.keyboards.reminder_keyboard import reminder_button
from aiogram import F, Router

time_pattern = r"^(1[0-7]:[0-5]\d|18:00)$"
logger = logging.getLogger(__name__)
booking_router = Router()

@booking_router.callback_query(lambda c: c.data.startswith("service_"))
@set_username
async def processes_services(callback: CallbackQuery, user_id, *args, **kwargs):
    service_id = int(callback.data.split("_")[2])
    service = await GetService(service_id=service_id).get()
    logger.info(f"Selected service: {service}. Type:{type(service)}")

    logger.info(f"Selected service: {service.name}. Type:{type(service.name)}")
    msg = template_manager.service_selection_info(service)
    free_date = await free_dates_keyboard("date")
    await callback.message.answer(
        text=msg,
        reply_markup=free_date,
    )
    set_user_data(user_id, service=service)
    logger.info(f"USER_DATA(handle_services) --- {get_user_data(user_id)}")
    await callback.answer()


@booking_router.callback_query(lambda c: c.data.startswith("date_date_"))
@check_user_data(["service"])
async def processes_dates(callback: CallbackQuery, user_id, *args, **kwargs):
    date_id = int(callback.data.split("_")[2])
    date = await GetFreeDate(date_id=date_id).get()
    logger.info(f"Selected date: {date.date}. Type:{type(date.date)}")
    msg = template_manager.date_selection_prompt(date)
    await callback.message.answer(text=msg)
    set_user_data(user_id, date=date)
    logger.info(f"USER_DATA(date_handler)---{get_user_data(user_id)}")
    await callback.answer()


@booking_router.message(F.text.regexp(time_pattern))
@check_user_data(["date", "service"])
async def processes_time(message: Message, user_id, *args, **kwars):
    logger.debug("Запуск обробника часу")  # Логування початку виконання функції
    time = message.text
    logger.info(f"User selected time: {time}")
    logger.info(f"USER DATE(processes_time) -- {user_data}")
    handlers = await handlers_time(user_id, time)
    if handlers is None:
        service, date = get_user_data(user_id, "service", "date")
        msg = template_manager.successful_booking_notification(service, date, time)
        await message.answer(text=msg, reply_markup=reminder_button)
        # user_data.pop(user_id)
    elif handlers[0] == False:
        _, msg = handlers
        await message.answer(text=msg)
    else:
        message_text, keyboard = handlers
        await message.answer(text=message_text, reply_markup=keyboard)


@booking_router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_the_entry(callback: CallbackQuery, user_id):
    time = callback.data.split("_")[-1]
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    logger.info(f"Time selected: {time} | type: {type(time)}")
    name, username, date, service = get_user_data(
        user_id, "name", "username", "date", "service"
    )
    await promote_booking(name, username, time, date, service, user_id)
    logger.info(f"SERVICE(in confirm_the_entry - {service})")
    msg = template_manager.successful_booking_notification(service, date, time.time())
    await callback.message.answer(text=msg, reply_markup=reminder_button)
    await callback.answer()
