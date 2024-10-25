from .models import FreeDate, Notes, session
from utils.format_datetime import NowDatetime
import logging
from decorators.adding_user_data import set_note_id

now = NowDatetime().now_datetime()
logger = logging.getLogger(__name__)


@set_note_id
async def add_notes(
    name: str,
    username: str,
    time: str,
    date: FreeDate,
    service,
    user_id: int,
    created_at=now,
):
    note = Notes(
        name=name,
        username=username,
        time=time,
        created_at=created_at,
        service_id=service.id,
        date_id=date.id,
        user_id=user_id,
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    logger.info(f"NOTE ID(in add_notes): {note.id}")
    return note
