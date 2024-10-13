from datetime import datetime, timedelta
from .db import session, get_service, get_notes, Notes, FreeDate
from utils.format_datetime import NowDatetime, FormatDate, FormatTime
from bot.keyboards import confirm_time_keyboard
from user_data import get_user_data

current_date_time = NowDatetime()
format_date = FormatDate()
format_time = FormatTime()


def get_busy_slots(user_id: int, date: FreeDate):
    user = get_user_data(user_id, 'service')
    durations = get_service(user.get('service').id)
    busy_slots = []
    for time in get_notes(date.id):
        time = format_time.formats_time_str_to_datetime(time.time)
        end_time = time + durations.durations
        start_time = time - durations.durations
        busy_slots.append({"start": start_time.time(), "end": end_time.time()})
        busy_slots = sorted(busy_slots, key=lambda slot: slot["start"])
    return busy_slots


def check_slot(user_id: int, date: FreeDate, time: datetime.time):
    busy_slots = get_busy_slots(user_id, date)
    for slot in busy_slots:
        if slot['start'] <= time.time() <= slot['end']:
            return find_nearest_available_time(time, busy_slots)
        else:
            return time


def date_check(user_id: int, time: datetime):
    user = get_user_data(user_id, 'date')
    date = user.get('date')
    now = current_date_time.now_datetime()
    if date.date == now.date():
        if time.time() > now.time():
            return check_slot(user_id, date, time)
    elif date.date > now.date():
        return check_slot(user_id, date, time)
    else:
        return None


def find_nearest_available_time(user_id: int, time: datetime.time, busy_slots: list):
    user = get_user_data(user_id, 'service')
    service_duration = get_service(user.get('service').durations)
    current_time = time
    for busy_slot in busy_slots:
        if busy_slot["start"] <= current_time < busy_slot["end"]:
            # Якщо вибраний час зайнятий, переносимо на кінець зайнятого часу
            current_time = busy_slot["end"]
        # Перевіряємо, чи є достатньо часу після поточного часу
        if current_time + service_duration <= busy_slot["start"]:
            return current_time.strftime("%H:%M")  # Повертаємо найближчий доступний час
    return current_time.strftime(
        "%H:%M"
    )  # Повертаємо, якщо час після останнього зайнятого


def add_notes(name: str, username: str, time: str, date:FreeDate, service, created_at=datetime.now()):
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


def handlers_time(user_id, time):
    time_str = time
    time = format_time.formats_time_str_to_datetime(time_str)
    now = current_date_time.now_datetime()
    
    nearest_time = date_check(user_id, time)
    if nearest_time == time:
        user = get_user_data(user_id, 'name', 'username', 'date', 'service')
        print(user)
        add_notes(user.get('name'), user.get('username'), time_str, user.get('date'), user.get('service'))
    else:
        keyboard = confirm_time_keyboard(nearest_time)
        return (
            f"Нажаль вказаний Вами час зайнятий. Найближчий доступний час: {nearest_time}. \nВиберіть цей час, або вкажіть інший",
            keyboard,
        )
