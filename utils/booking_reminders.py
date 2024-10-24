from db.db_reader import GetNotes
from datetime import datetime, timedelta
from utils.format_datetime import NowDatetime
from utils.message_templates import template_manager
from utils.message_sender import manager


async def find_time_for_reminder():
    active_notes = GetNotes(only_active=True).get_all_notes()
    now = NowDatetime().now_datetime()

    for note in active_notes:
        if not note.reminder_hours:
            continue  # Повідомлення не повинно бути відправлене

        reminder_hours = note.reminder_hours
        note_time = datetime.combine(note.free_date.date, note.time)
        reminder_time = note_time - timedelta(hours=reminder_hours)

        if abs((now - reminder_time).total_seconds()) <= 600:  # 10 хвилин в секундах
            msg = template_manager.recording_reminder(note)
            await manager.send_message(chat_id=note.user_id, message=msg)
