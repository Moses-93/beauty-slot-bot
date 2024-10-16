import logging
from db.queries import add_notes
from bot.keyboards import confirm_time_keyboard
from user_data import get_user_data
from .time_processing import date_check, time_check, format_time


logger = logging.getLogger(__name__)


def handlers_time(user_id: int, time: str):
    name, username, date, service = get_user_data(
        user_id, "name", "username", "date", "service"
    )
    logger.info(
        f"NAME - {name}, USERNAME - {username}, DATE - {date}, SERVICE - {service}"
    )
    time_str = time
    time = format_time.formats_time_str_to_datetime(time_str)
    if time_check(time, date) == False:
        message = f"Ви не можете обрати {time_str}, оскільки він вже пройшов"
        logger.info("handlers_time ПОВЕРНУВ False, message")
        return False, message
    nearest_time = date_check(user_id, time)
    logger.info(f"nearest_time {nearest_time}")
    if nearest_time == time:
        logger.info(f"handlers_time ВИКЛИКАВ add_notes ДЛЯ ЗАПИСУ В БД")
        add_notes(name, username, time_str, date, service, user_id)
    else:
        keyboard = confirm_time_keyboard(nearest_time)
        logger.info("handlers_time ПОВЕРНУВ True, message")
        return (
            f"Нажаль, вказаний Вами час зайнятий. Найближчий доступний час: {nearest_time}. \nОберіть цей час, або вкажіть інший",
            keyboard,
        )
