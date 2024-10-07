from datetime import datetime
from .db import session, Notes, Service
from bot.keyboards import confirm_time_keyboard


def find_nearest_available_time(start_time, busy_slots, service_duration):
    current_time = start_time
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


def free_hours(time: str, date: str, service_id):
    if time and date is not None:
        service = session.query(Service).filter(Service.id == service_id).first().durations
        busy_notes = session.query(Notes).filter(Notes.date == date)

        # Формуємо список зайнятих слотів часу
        busy_slots = []
        for note in busy_notes:
            start_time = datetime.strptime(note.time, "%H:%M")
            end_time = start_time + service
            busy_slots.append({"start": start_time, "end": end_time})
            # Сортуємо зайняті слоти за часом початку
            busy_slots = sorted(busy_slots, key=lambda slot: slot["start"])


        # Перевіряємо час, який обрав користувач
        selected_time = datetime.strptime(time, "%H:%M")
        for slot in busy_slots:
            if slot["start"] <= selected_time < slot["end"]:
                # Якщо час зайнятий, шукаємо найближчий вільний
                nearest_time = find_nearest_available_time(
                    selected_time, busy_slots, service
                )
                return nearest_time
        return time


def add_notes(name, username, time, date, service, created_at=datetime.now()):
    note = Notes(
        name=name,
        phone=username,
        time=time,
        created_at=created_at,
        service_id=service.id,
        date=date,
    )
    session.add(note)
    session.commit()
    session.refresh(note)


def handlers_time(name, username, time, user_id, user_data):
    try:
        date = user_data[user_id].get("date")
        service = user_data[user_id].get("service")
    except KeyError:
        return "Спочатку виберіть послугу та дату"
    nearest_time = free_hours(time, date.date, service.id)
    if nearest_time == time:
        user_data[user_id]["time"] = nearest_time
        add_notes(name, username, time, date.date, service)
    else:
        keyboard = confirm_time_keyboard(nearest_time)
        return f"Нажаль вказаний Вами час зайнятий. Найближчий доступний час: {nearest_time}. \nВиберіть цей час, або вкажіть інший", keyboard
