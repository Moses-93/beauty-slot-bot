from datetime import datetime
import logging
from db.db_writer import add_notes
from bot.keyboards import confirm_time_keyboard
from user_data import get_user_data
from .time_processing import check_slot, time_check, format_time
from .message_sender import manager
from .message_templates import template_manager
from db.models import FreeDate, Service
from os import getenv

USER_ID = getenv("USER_ID_MASTER")


logger = logging.getLogger(__name__)


async def promote_booking(
    name: str, username: str, time, date: FreeDate, service: Service, user_id: int
):
    """Проміжна функція для запису в БД та відправлення повідоомлень користувачу та майстру"""
    await add_notes(name, username, time, date, service, user_id)
    msg_for_master = template_manager.message_to_the_master(
        username, service, date, time
    )
    await manager.send_message(USER_ID, msg_for_master)
    msg_for_user = template_manager.get_booking_confirmation(service, date, time)
    await manager.send_message(user_id, msg_for_user)


async def handlers_time(user_id: int, time: str):
    name, username, date, service = get_user_data(
        user_id, "name", "username", "date", "service"
    )
    logger.info(
        f"NAME - {name}, USERNAME - {username}, DATE - {date}, SERVICE - {service}"
    )
    time = format_time.formats_time_str_to_datetime(time).time()
    time = datetime.combine(date.date, time)
    if time_check(time) == False:
        message = template_manager.elapsed_time_warning(time)
        logger.warning("handlers_time - Час, який обрав користувач вже пройшов")
        return False, message

    nearest_time = check_slot(user_id, time)
    logger.info(f"nearest_time {nearest_time}")
    logger.info(f"time {time}")

    if nearest_time == time:
        logger.info(
            f"handlers_time ВИКЛИКАВ promote_booking ДЛЯ ЗАПИСУ В БД ТА ВІДПРАЛЕННЯ ПООВІДОМЛЕННЯ"
        )
        await promote_booking(name, username, time, date, service, user_id)

    else:
        keyboard = confirm_time_keyboard(nearest_time)
        logger.info(
            "handlers_time Час, який обрав користувач - зайнятий, повернулась пропозиція з часом"
        )
        msg = template_manager.busy_time_notification(nearest_time)
        return (msg, keyboard)
