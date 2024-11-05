from datetime import datetime
from sqlalchemy import and_, or_, select
from .models import Service, FreeDate, Notes, async_session
from utils.format_datetime import NowDatetime, FormatTime
import logging
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload

logger = logging.getLogger(__name__)

now = NowDatetime().now_datetime()
format_time = FormatTime()


class ServiceRepository:

    @staticmethod
    async def get_service_by_id(service_id: int):
        async with async_session() as session:
            result = await session.execute(select(Service).filter_by(id=service_id))
            return result.scalar()

    @staticmethod
    async def get_service_by_name(name: str):
        async with async_session() as session:
            result = await session.execute(select(Service).filter_by(name=name))
            return result.scalar()

    @staticmethod
    async def get_all_services():
        async with async_session() as session:
            result = await session.execute(select(Service))
            return result.scalars().all()


class FreeDateRepository:

    @staticmethod
    async def get_free_dates_by_date_id(date_id):
        async with async_session() as session:
            result = await session.execute(select(FreeDate).filter_by(id=date_id))
            return result.scalar()

    @staticmethod
    async def get_free_date_by_date(date):
        async with async_session() as session:
            result = await session.execute(select(FreeDate).filter_by(date=date))
            return result.scalar()

    @staticmethod
    async def get_all_free_dates():
        async with async_session() as session:
            result = await session.execute(
                select(FreeDate).filter(FreeDate.free.is_(True), FreeDate.now > now)
            )
            return result.scalars().all()


class NotesRepository:

    async def get_filtered_notes(session, user_id=None, date_id=None):
        query = select(Notes).options(selectinload(Notes.service), selectinload(Notes.free_date))

        if user_id:
            query = query.filter(Notes.user_id == user_id)
        if date_id:
            query = query.filter(Notes.date_id == date_id)
        
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
    async def get_filtered_active_notes(session, user_id=None, note_id=None, now=datetime.now()):
        # Створюємо запит з жадним завантаженням (joinedload) для пов'язаних моделей
        query = (
            select(Notes)
            .join(FreeDate, FreeDate.id == Notes.date_id)
            .options(
                joinedload(Notes.service),      # Жадне завантаження для зв'язку з Service
                joinedload(Notes.free_date)     # Жадне завантаження для зв'язку з FreeDate
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
    async def get_all_active_notes():
        async with async_session() as session:  # Використовуйте асинхронну сесію
            return await NotesRepository.get_filtered_active_notes(session)

    @staticmethod
    async def get_active_notes_by_user_id(user_id: int):
        async with async_session() as session:
            return await NotesRepository.get_filtered_active_notes(session, user_id=user_id)

    @staticmethod
    async def get_active_notes_by_note_id(note_id: int):
        async with async_session() as session:
            return await NotesRepository.get_filtered_active_notes(session, note_id=note_id)


class NotesDeleteRepository:

    @staticmethod
    async def delete_notes_by_note_id(note_id: int):
        async with async_session() as session:
            note = await session.get(Notes, note_id)
            if note:
                await session.delete(note)
                await session.commit()


class UpdateNotesRepository:

    @staticmethod
    async def update_reminder(note_id, reminder_hours: int):
        logging.info(
            f"UPDATING REMINDER: {reminder_hours} | type: {type(reminder_hours)}"
        )
        async with async_session() as session:
            result = await session.get(Notes, note_id)
            if result:
                logging.info(f"RESULT BEFORE: {reminder_hours}")
                result.reminder_hours = reminder_hours
                logging.info(f"RESULT AFTER: {reminder_hours}")

                await session.commit()
