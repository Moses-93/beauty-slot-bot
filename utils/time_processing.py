import logging
from utils.format_datetime import NowDatetime, FormatDate, FormatTime
from user_data import get_user_data
from db.models import FreeDate
from db.db_reader import GetService, GetNotes
from datetime import datetime


current_date_time = NowDatetime()
format_date = FormatDate()
format_time = FormatTime()


logger = logging.getLogger(__name__)


def get_busy_slots(user_id: int):
    service, date = get_user_data(user_id, "service", "date")
    logger.info(f"SERVICE -- {service}")
    busy_slots = []
    notes = GetNotes(date_id=date.id).get_all_notes()
    logger.info(f"NOTES -- {notes}")
    for time in notes:
        time = datetime.combine(date.date, time.time)
        end_time = time + service.durations
        start_time = time - service.durations
        busy_slots.append({"start": start_time, "end": end_time})
        busy_slots = sorted(busy_slots, key=lambda slot: slot["start"])
    logger.info(f"get_busy_slots ПОВЕРНУВ {busy_slots}")
    return busy_slots


def find_nearest_available_time(user_id: int, time: datetime, busy_slots: list):
    (service,) = get_user_data(user_id, "service")
    current_time = time
    logger.info(f"CURRENT_TIME: - {current_time}")

    for busy_slot in busy_slots:
        logger.info(f"BUSY SLOTS: - {busy_slot}")
        logger.info(f"СТАРТОВИЙ ЧАС: {busy_slot['start'].time()}")
        logger.info(f"КІНЦЕВИЙ ЧАС: {busy_slot['end'].time()}")

        if busy_slot["start"] <= current_time <= busy_slot["end"]:
            logger.info(
                f"УВІЙШЛИ В УМОВНУ ПЕРЕВІРКУ."
            )
            # Якщо вибраний час зайнятий, переносимо на кінець зайнятого часу
            current_time = busy_slot["end"]
            logger.info(f"CURRENT TIME ПІСЛЯ ПРИСВОЄННЯ: {current_time}")
        # Перевіряємо, чи є достатньо часу після поточного часу
    if current_time + service.durations <= busy_slot["start"]:
        logger.info(
            f"find_nearest_available_time ПОВЕРНУВ ПІСЛЯ ІТЕРАЦІЇ: {current_time}"
        )
        return current_time.time() # Повертаємо найближчий доступний час
    logger.info(f"find_nearest_available_time ПОВЕРНУВ {current_time}")
    return current_time.time()


def check_slot(user_id: int, time: datetime):
    busy_slots = get_busy_slots(user_id)
    if busy_slots:
        logger.info(f"TIME(in check_slot) -- {time}")
        for slot in busy_slots:
            if slot["start"] <= time <= slot["end"]:
                logger.info(f"check_slot ВИКЛИКАВ find_nearest_available_time")
                return find_nearest_available_time(user_id, time, busy_slots)

        logger.info(f"check_slot ПОВЕРНУВ {time} ПІСЛЯ ІТЕРАЦІЇ")
        return time.time()
    else:
        logger.info(f"check_slot ПОВЕРНУВ {time}")
        return time.time()


def time_check(date_time: datetime):
    now = current_date_time.now_datetime()
    logger.info(f"NOW(in time_check): {now}")
    logger.info(f"DATE_TIME(in time_check): {date_time}")
    if date_time < now:
        return False
