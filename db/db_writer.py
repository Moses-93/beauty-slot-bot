import logging
from sqlalchemy import select
from .models import Admins, Dates, Notes, Services
from .config import async_session
from decorators.caching.user_cache import cache_note_id

logger = logging.getLogger(__name__)


class NotesManager:

    def __init__(self, async_session) -> None:
        self.async_session = async_session

    @cache_note_id
    async def create(self, **kwargs):
        note = Notes(**kwargs)
        async with self.async_session() as session:
            session.add(note)
            await session.commit()
            await session.refresh(note)
            logger.info(f"NOTE ID(in create): {note.id}")
            return note

    async def update_reminder(self, note_id: int, reminder_hours: int):
        logger.info("Запуск методу для оновлення поля нагадування")
        async with async_session() as session:
            result = await session.get(Notes, note_id)
            if result:
                result.reminder_hours = reminder_hours
                await session.commit()

    async def delete(self, note_id: int):
        async with async_session() as session:
            note = await session.get(Notes, note_id)
            if note:
                await session.delete(note)
                await session.commit()


class ServiceManager:
    def __init__(self, async_session) -> None:
        self.async_session = async_session

    async def create(self, **kwargs):
        new_service = Services(**kwargs)
        async with self.async_session() as session:
            session.add(new_service)
            await session.commit()
            await session.refresh(new_service)

    async def update(self, service_id, **kwargs):
        async with self.async_session() as session:
            updated_service = await session.execute(
                select(Services).filter_by(id=service_id)
            )
            service = updated_service.scalars().first()
            if service:
                for key, value in kwargs.items():
                    setattr(service, key, value)
                await session.commit()

    async def delete(self, service_id):
        async with self.async_session() as session:
            service = await session.get(Services, service_id)
            if service:
                await session.delete(service)
                await session.commit()


class DatesManager:
    def __init__(self, async_session) -> None:
        self.async_session = async_session

    async def create(self, **kwargs):
        new_date = Dates(**kwargs)
        async with self.async_session() as session:
            session.add(new_date)
            await session.commit()
            await session.refresh(new_date)

    async def delete(self, date_id):
        async with self.async_session() as session:
            date = await session.get(Dates, date_id)
            if date:
                await session.delete(date)
                await session.commit()


class AdminsManager:

    def __init__(self, async_session) -> None:
        self.async_session = async_session

    async def create(self, **kwargs):
        async with self.async_session() as session:
            admin = Admins(**kwargs)
            session.add(admin)
            await session.commit()
            await session.refresh(admin)

    async def delete(self, admin_id):
        async with self.async_session() as session:
            admin = await session.get(Admins, admin_id)
            if admin:
                await session.delete(admin)
                await session.commit()


admins_manager = AdminsManager(async_session)
service_manager = ServiceManager(async_session)
date_manager = DatesManager(async_session)
notes_manager = NotesManager(async_session)
