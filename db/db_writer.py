from .models import FreeDate, Notes, Service, session
from utils.format_datetime import NowDatetime
import logging
from decorators.adding_user_data import set_note_id
from sqlalchemy.ext.asyncio import AsyncSession

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


class ServiceManager:
    def __init__(self, session) -> None:
        self.session = session

    async def create(self, **kwargs):
        new_service = Service(**kwargs)
        self.session.add(new_service)
        self.session.commit()
        self.session.refresh(new_service)

    async def update(self, service_id, **kwargs):
        updated_service = self.session.query(Service).filter_by(id=service_id)
        updated_service.update(kwargs)
        self.session.commit()

    async def delete(self, service_id):
        service = self.session.query(Service).filter_by(id=service_id).delete()
        self.session.commit()
        return service


class FreeDatesManager:
    def __init__(self, session) -> None:
        self.session = session

    async def create(self, **kwargs):
        new_date = FreeDate(**kwargs)
        self.session.add(new_date)
        self.session.commit()
        self.session.refresh(new_date)

    async def delete(self, date_id):
        date = self.session.query(FreeDate).filter_by(id=date_id).delete()
        self.session.commit()
        return date


service_manager = ServiceManager(session)
date_manager = FreeDatesManager(session)
