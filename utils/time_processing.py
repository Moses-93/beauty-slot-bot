import logging
from utils.format_datetime import NowDatetime, FormatDate, FormatTime
from user_data import get_user_data
from db.models import FreeDate
from db.commands import GetService, GetNotes
from datetime import datetime


current_date_time = NowDatetime()
format_date = FormatDate()
format_time = FormatTime()


logger = logging.getLogger(__name__)


def get_busy_slots(user_id: int, date: FreeDate):
    (service,) = get_user_data(user_id, "service")
    logger.info(f"SERVICE -- {service}")
    busy_slots = []
    notes = GetNotes(date_id=date.id).get_all_notes()
    logger.info(f"NOTES -- {notes}")
    for time in notes:
        time = format_time.formats_time_str_to_datetime(time.time)
        end_time = time + service.durations
        start_time = time - service.durations
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
    (date,) = get_user_data(user_id, "date")
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
    (service,) = get_user_data(user_id, "service")
    current_time = time
    for busy_slot in busy_slots:
        if busy_slot["start"].time() <= current_time.time() < busy_slot["end"].time():
            # Якщо вибраний час зайнятий, переносимо на кінець зайнятого часу
            current_time = busy_slot["end"]
        # Перевіряємо, чи є достатньо часу після поточного часу
        if current_time + service.durations <= busy_slot["start"]:
            logger.info(f"find_nearest_available_time ПОВЕРНУВ {current_time}")
            return format_time.formats_datetime_to_time_str(
                current_time
            )  # Повертаємо найближчий доступний час
    logger.info(f"find_nearest_available_time ПОВЕРНУВ {current_time}")
    return format_time.formats_datetime_to_time_str(
        current_time
    )  # Повертаємо, якщо час після останнього зайнятого


def time_check(time: datetime, date: FreeDate):
    now = current_date_time.now_datetime()
    combine_datetime = datetime.combine(date.date, time.time())
    if combine_datetime < now:
        return False
