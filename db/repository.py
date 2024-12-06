import logging
from datetime import datetime
from .models import Services, Dates, Notes, Admins
from .config import async_session, AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, select, update
from .interfaces import (
    GetNotesInterface,
    GetDatesInterface,
    GetServicesInterface,
    GetAdminsInterface,
)


logger = logging.getLogger(__name__)


class BaseGetNotes(GetNotesInterface):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _deactivate_old_notes(self, session: AsyncSession):
        logger.info("Запуск методу для деактивації старих записів")
        now = datetime.now()
        stmt = (
            update(Notes)
            .where(
                Notes.active == True,
                Notes.time < now.time(),
                Notes.date.has(Dates.date <= now.date()),
            )
            .values(active=False)
        )
        await session.execute(stmt)
        await session.commit()

    async def get_notes(self, *expressions, **filters):
        logger.info("Запуск методу для отримання записів")
        async with self.session() as session:
            if filters.get("active"):
                await self._deactivate_old_notes(session)
            query = select(Notes).options(
                selectinload(Notes.service), selectinload(Notes.date)
            )
            if expressions:
                query = query.filter(Notes.date.has(and_(*expressions)))
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()


class BaseGetServices(GetServicesInterface):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_service(self, **filters):
        logger.info("Запуск методу для отримання послуг")
        async with self.session() as session:
            query = select(Services)
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()


class BaseGetDates(GetDatesInterface):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def deactivate_old_date(self, session: AsyncSession):
        logger.info("Запуск методу для деактивації старих дат")
        now = datetime.now()
        stmt = (
            update(Dates)
            .where(
                Dates.free == True,
                Dates.del_time < now,
            )
            .values(free=False)
        )
        await session.execute(stmt)
        await session.commit()

    async def get_date(self, **filters):
        logger.info("Запит для отримання дат")
        async with self.session() as session:
            if filters.get("free"):
                await self.deactivate_old_date(session)
            query = select(Dates)
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()


class BaseGetAdmins(GetAdminsInterface):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_admins(self, **filters):
        async with self.session() as session:
            query = select(Admins)
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()


base_get_admins = BaseGetAdmins(async_session)
base_get_free_date = BaseGetDates(async_session)
base_get_service = BaseGetServices(async_session)
base_get_notes = BaseGetNotes(async_session)
