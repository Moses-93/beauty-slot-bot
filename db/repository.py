from datetime import datetime, timedelta
from sqlalchemy import and_, or_, select
from .models import Service, FreeDate, Notes, async_session
import logging
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload

logger = logging.getLogger(__name__)


class ServiceRepository:

    async def get_filtered_services(
        session, service_id: int = None, service_name: str = None
    ):
        query = select(Service)
        if service_id:
            query = query.filter(Service.id == service_id)
        if service_name:
            query = query.filter(Service.name == service_name)
        result = await session.execute(query)
        return result.scalar()

    @staticmethod
    async def get_service_by_id(service_id: int):
        async with async_session() as session:
            return await ServiceRepository.get_filtered_services(session, service_id)

    @staticmethod
    async def get_service_by_name(name: str):
        async with async_session() as session:
            return await ServiceRepository.get_filtered_services(
                session, service_name=name
            )

    @staticmethod
    async def get_all_services():
        async with async_session() as session:
            result = await session.execute(select(Service))
            return result.scalars().all()


class FreeDateRepository:

    @staticmethod
    async def get_filtered_dates(session, **filters: int | datetime | str | bool):
        query = select(FreeDate)
        if filters.get("date_id"):
            query = query.filter(FreeDate.id == filters.get("date_id"))
        if filters.get("date"):
            query = query.filter(FreeDate.date == filters.get("date"))
        if filters.get("free"):
            now = filters.get("now")
            query = query.filter(FreeDate.free.is_(True), FreeDate.now > now)
        result = await session.execute(query)
        return result.scalars().all() if filters.get("free") else result.scalar()

    @staticmethod
    async def get_free_dates_by_date_id(date_id):
        async with async_session() as session:
            return await FreeDateRepository.get_filtered_dates(session, date_id=date_id)

    @staticmethod
    async def get_free_date_by_date(date: datetime):
        async with async_session() as session:
            return await FreeDateRepository.get_filtered_dates(session, date=date)

    @staticmethod
    async def get_all_free_dates(now: datetime):
        async with async_session() as session:
            return await FreeDateRepository.get_filtered_dates(
                session, free=True, now=now
            )

    @staticmethod
    async def get_dates_last_30_days(now: datetime):
        async with async_session() as session:
            query = select(FreeDate).filter(FreeDate.date >= now - timedelta(days=30))
            result = await session.execute(query)
            return result.scalars().all()


class NotesRepository:

    @staticmethod
    async def get_filtered_notes(session, user_id=None, date_id=None, service_id=None):
        query = select(Notes).options(
            selectinload(Notes.service), selectinload(Notes.free_date)
        )

        if user_id:
            query = query.filter(Notes.user_id == user_id)
        if date_id:
            query = query.filter(Notes.date_id == date_id)
        if service_id:
            query = query.filter(Notes.service_id == service_id)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_notes_by_user_id(user_id: int):
        async with async_session() as session:
            return await NotesRepository.get_filtered_notes(session, user_id=user_id)

    @staticmethod
    async def get_notes_by_date_id(date_id: int):
        async with async_session() as session:
            return await NotesRepository.get_filtered_notes(session, date_id=date_id)

    @staticmethod
    async def get_notes_by_service_id(service_id: int):
        async with async_session() as session:
            return await NotesRepository.get_filtered_notes(
                session, service_id=service_id
            )

    @staticmethod
    async def get_filtered_active_notes(
        session, now: datetime, user_id: int = None, note_id: int = None
    ):
        # Створюємо запит з жадним завантаженням (joinedload) для пов'язаних моделей
        query = (
            select(Notes)
            .join(FreeDate, FreeDate.id == Notes.date_id)
            .options(
                joinedload(Notes.service),  # Жадне завантаження для зв'язку з Service
                joinedload(
                    Notes.free_date
                ),  # Жадне завантаження для зв'язку з FreeDate
            )
            .filter(
                or_(
                    FreeDate.date > now.date(),
                    and_(
                        FreeDate.date == now.date(),
                        Notes.time > now.time(),
                    ),
                )
            )
        )

        # Додаємо фільтрацію за user_id, якщо задано
        if user_id:
            query = query.filter(Notes.user_id == user_id)

        # Додаємо фільтрацію за note_id, якщо задано
        if note_id:
            query = query.filter(Notes.id == note_id)

        # Виконуємо запит і повертаємо результат
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_notes_by_days(day: int):
        async with async_session() as session:
            # Визначаємо стартову дату фільтрації
            start_time = datetime.now() - timedelta(days=day)
            # Створюємо запит з жадним завантаженням
            query = (
                select(Notes)
                .join(FreeDate, FreeDate.id == Notes.date_id)
                .options(
                    joinedload(Notes.free_date), joinedload(Notes.service)
                )  # Жадне завантаження
                .filter(FreeDate.date >= start_time.date())
            )
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_all_active_notes(now: datetime):
        async with async_session() as session:  # Використовуйте асинхронну сесію
            return await NotesRepository.get_filtered_active_notes(session, now)

    @staticmethod
    async def get_active_notes_by_user_id(user_id: int, now: datetime):
        async with async_session() as session:
            return await NotesRepository.get_filtered_active_notes(
                session, now, user_id=user_id
            )

    @staticmethod
    async def get_active_notes_by_note_id(note_id: int, now: datetime):
        async with async_session() as session:
            return await NotesRepository.get_filtered_active_notes(
                session, now, note_id=note_id
            )
