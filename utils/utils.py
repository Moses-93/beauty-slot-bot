from datetime import datetime
import logging
from .db import session, get_service, get_notes, Notes, FreeDate
from utils.format_datetime import NowDatetime, FormatDate, FormatTime
from bot.keyboards import confirm_time_keyboard
from user_data import get_user_data

current_date_time = NowDatetime()
format_date = FormatDate()
format_time = FormatTime()

logger = logging.getLogger(__name__)


def get_busy_slots(user_id: int, date: FreeDate):
    user = get_user_data(user_id, "service")
    durations = get_service(user.get("service").id)
    busy_slots = []
    for time in get_notes(date.id):
        time = format_time.formats_time_str_to_datetime(time.time)
        end_time = time + durations.durations
        start_time = time - durations.durations
        busy_slots.append({"start": start_time, "end": end_time})
        busy_slots = sorted(busy_slots, key=lambda slot: slot["start"])
    logger.info(f"get_busy_slots ПОВЕРНУВ {busy_slots}")
    return busy_slots


def check_slot(user_id: int, date: FreeDate, time: datetime.time):
    busy_slots = get_busy_slots(user_id, date)
    if busy_slots:
        for slot in busy_slots:
            if slot["start"].time() <= time.time() <= slot["end"].time():
                logger.info(f"check_slot ВИКЛИКАВ find_nearest_available_time")
                return find_nearest_available_time(user_id, time, busy_slots)

        logger.info(f"check_slot ПОВЕРНУВ {time} ПІСЛЯ ІТЕРАЦІЇ")
        return time
    else:
        logger.info(f"check_slot ПОВЕРНУВ {time}")
        return time


def date_check(user_id: int, time: datetime):
    user = get_user_data(user_id, "date")
    date = user.get("date")
    now = current_date_time.now_datetime()
    if date.date == now.date():
        if time.time() > now.time():
            logger.info(f"date_check ВИКЛИКАВ check_slot для теперішньої дати")
            return check_slot(user_id, date, time)
    elif date.date > now.date():
        logger.info(f"date_check ВИКЛИКАВ check_slot для майбутньої дати")
        return check_slot(user_id, date, time)
    else:
        logger.info(f"date_check ПОВЕРНУВ None")
        return None


def find_nearest_available_time(user_id: int, time: datetime, busy_slots: list):
    user = get_user_data(user_id, "service")
    service_duration = get_service(user.get("service").id)
    current_time = time
    for busy_slot in busy_slots:
        if busy_slot["start"].time() <= current_time.time() < busy_slot["end"].time():
            # Якщо вибраний час зайнятий, переносимо на кінець зайнятого часу
            current_time = busy_slot["end"]
        # Перевіряємо, чи є достатньо часу після поточного часу
        if current_time + service_duration.durations <= busy_slot["start"]:
            logger.info(f"find_nearest_available_time ПОВЕРНУВ {current_time}")
            return current_time.strftime("%H:%M")  # Повертаємо найближчий доступний час
    logger.info(f"find_nearest_available_time ПОВЕРНУВ {current_time}")
    return current_time.strftime(
        "%H:%M"
    )  # Повертаємо, якщо час після останнього зайнятого


def add_notes(
    name: str,
    username: str,
    time: str,
    date: FreeDate,
    service,
    created_at=datetime.now(),
):
    note = Notes(
        name=name,
        username=username,
        time=time,
        created_at=created_at,
        service_id=service.id,
        date_id=date.id,
    )
    session.add(note)
    session.commit()
    session.refresh(note)


def time_check(time: datetime, date: FreeDate):
    now = current_date_time.now_datetime()
    combine_datetime = datetime.combine(date.date, time.time())
    if combine_datetime < now:
        return False


def handlers_time(user_id: int, time: str):
    user = get_user_data(user_id, "name", "username", "date", "service")
    time_str = time
    time = format_time.formats_time_str_to_datetime(time_str)
    if time_check(time, user.get("date")) == False:
        message = f"Ви не можете обрати {time_str}, оскільки він вже пройшов"
        logger.info("handlers_time ПОВЕРНУВ False, message")
        return False, message
    nearest_time = date_check(user_id, time)
    logger.info(f"nearest_time {nearest_time}")
    if nearest_time == time:
        logger.info(f"handlers_time ВИКЛИКАВ add_notes ДЛЯ ЗАПИСУ В БД")
        add_notes(
            user.get("name"),
            user.get("username"),
            time_str,
            user.get("date"),
            user.get("service"),
        )
    else:
        keyboard = confirm_time_keyboard(nearest_time)
        logger.info("handlers_time ПОВЕРНУВ True, message")
        return (
            f"Нажаль, вказаний Вами час зайнятий. Найближчий доступний час: {nearest_time}. \nОберіть цей час, або вкажіть інший",
            keyboard,
        )
