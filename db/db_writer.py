from sqlalchemy import select
from .models import FreeDate, Notes, Service, async_session
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
    async with async_session() as session:
        session.add(note)
        await session.commit()
        await session.refresh(note)
        logger.info(f"NOTE ID(in add_notes): {note.id}")
        return note


class ServiceManager:
    def __init__(self, async_session) -> None:
        self.async_session = async_session

    async def create(self, **kwargs):
        new_service = Service(**kwargs)
        async with self.async_session() as session:
            session.add(new_service)
            await session.commit()
            await session.refresh(new_service)

    async def update(self, service_id, **kwargs):
        async with self.async_session() as session:
            updated_service = await session.execute(
                select(Service).filter_by(id=service_id)
            )
            service = updated_service.scalars().first()
            if service:
                for key, value in kwargs.items():
                    setattr(service, key, value)
                await session.commit()

    async def delete(self, service_id):
        async with self.async_session() as session:
            service = await session.get(Service, service_id)
            if service:
                await session.delete(service)
                await session.commit()


class FreeDatesManager:
    def __init__(self, async_session) -> None:
        self.async_session = async_session

    async def create(self, **kwargs):
        new_date = FreeDate(**kwargs)
        async with self.async_session() as session:
            session.add(new_date)
            await session.commit()
            await session.refresh(new_date)

    async def delete(self, date_id):
        async with self.async_session() as session:
            date = await session.get(FreeDate, date_id)
            if date:
                await session.delete(date)
                await session.commit()


service_manager = ServiceManager(async_session)
date_manager = FreeDatesManager(async_session)
