import logging

from datetime import datetime, timedelta

from src.db.crud import notes_manager

from src.db.models import Booking

from src.utils.message_templates import template_manager
from src.utils.message_sender import manager


logger = logging.getLogger(__name__)


async def find_time_for_reminder():
    now = datetime.now()
    active_notes = await notes_manager.read(
        relations=(
            Booking.date,
            Booking.service,
        ),
        active=True,
    )

    for note in active_notes:
        if not note.reminder_time:
            continue  # Повідомлення не повинно бути відправлене

        reminder_time = note.reminder_time
        note_time = datetime.combine(note.date.date, note.time)
        reminder_time = note_time - timedelta(hours=reminder_time)

        if abs((now - reminder_time).total_seconds()) <= 600:  # 10 хвилин в секундах
            msg = template_manager.get_reminder(note=note)
            logger.info(
                f"Нагадування відправлено користувачу: {note.username if note.username else note.name}"
            )
            await manager.send_message(chat_id=note.user_id, message=msg)
