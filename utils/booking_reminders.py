import logging
from db.db_reader import get_notes
from datetime import datetime, timedelta
from utils.message_templates import template_manager
from utils.message_sender import manager

logger = logging.getLogger(__name__)


async def find_time_for_reminder():
    now = datetime.now()
    active_notes = await get_notes.get_notes(active=True)

    for note in active_notes:
        if not note.reminder_hours:
            continue  # Повідомлення не повинно бути відправлене

        reminder_hours = note.reminder_hours
        note_time = datetime.combine(note.free_date.date, note.time)
        reminder_time = note_time - timedelta(hours=reminder_hours)

        if abs((now - reminder_time).total_seconds()) <= 600:  # 10 хвилин в секундах
            msg = template_manager.get_reminder(note=note)
            logger.info(
                f"Нагадування відправлено користувачу: {note.username if note.username else note.name}"
            )
            await manager.send_message(chat_id=note.user_id, message=msg)
