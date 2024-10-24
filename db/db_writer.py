from .models import FreeDate, Notes, session
from utils.format_datetime import NowDatetime

now = NowDatetime().now_datetime()

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
