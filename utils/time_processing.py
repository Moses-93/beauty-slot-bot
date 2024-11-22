import logging
from utils.format_datetime import FormatDate, FormatTime
from cache.cache import user_cache
from db.db_reader import GetNotes
from datetime import datetime


format_date = FormatDate()
format_time = FormatTime()


logger = logging.getLogger(__name__)


async def get_busy_slots(user_id: int):
    logger.info("Запуск функції для пошуку зайнятих слотів")
    service, date = await user_cache.get_user_cache(user_id, "service", "date")
    busy_slots = []
    notes = await GetNotes(date_id=date.id).get_notes()
    for time in notes:
        time = datetime.combine(date.date, time.time)
        end_time = time + service.durations
        start_time = time - service.durations
        busy_slots.append({"start": start_time, "end": end_time})
        busy_slots = sorted(busy_slots, key=lambda slot: slot["start"])
    logger.info(f"Повернуто: {busy_slots}")
    return busy_slots


async def find_nearest_available_time(user_id: int, time: datetime, busy_slots: list):
    logger.info("Запуск функції для знаходження найближчого доступного часу")
    (service,) = await user_cache.get_user_cache(user_id, "service")
    current_time = time
    logger.info(f"CURRENT_TIME: - {current_time}")

    for busy_slot in busy_slots:

        if busy_slot["start"] <= current_time <= busy_slot["end"]:
            # Якщо вибраний час зайнятий, переносимо на кінець зайнятого часу
            current_time = busy_slot["end"]
        # Перевіряємо, чи є достатньо часу після поточного часу
    if current_time + service.durations <= busy_slot["start"]:
        logger.info(f"Повернуто: {current_time}")
        return current_time  # Повертаємо найближчий доступний час
    logger.info(f"Повернуто: {current_time}")
    return current_time


async def check_slot(user_id: int, time: datetime):
    logger.info("Запуск функції для перевірки доступності часу")
    busy_slots = await get_busy_slots(user_id)
    if busy_slots:
        logger.info(f"Час:{time}")
        for slot in busy_slots:
            if slot["start"] <= time <= slot["end"]:
                return await find_nearest_available_time(user_id, time, busy_slots)

        logger.info(f"Повернуто: {time}")
        return time
    else:
        logger.info(f"Повернуто: {time}")
        return time


async def time_check(date_time: datetime):
    now = datetime.now()
    if date_time < now:
        logger.warning("Час, який обрав користувач вже пройшов")
        return False
