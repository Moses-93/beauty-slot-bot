from sqlalchemy import and_, or_, select
from .models import Service, FreeDate, Notes, async_session
from utils.format_datetime import NowDatetime, FormatTime

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
            result = await session.execute(select(FreeDate).filter(
            FreeDate.free.is_(True), FreeDate.now > now))
            return result.scalars().all()


class NotesRepository:

    @staticmethod
    async def get_notes_by_user_id(user_id: int):
        async with async_session() as session:
            result = await session.execute(select(Notes).filter_by(user_id=user_id))
            return result.scalars().all()

    @staticmethod
    async def get_notes_by_date_id(date_id: int):
        async with async_session() as session:
            result = await session.execute(select(Notes).filter_by(date_id=date_id))
            return result.scalars().all()

    @staticmethod
    async def get_all_active_notes(now):
        async with async_session() as session:  # Використовуйте асинхронну сесію
            result = await session.execute(
                select(Notes).join(FreeDate, FreeDate.id == Notes.date_id).filter(
                    or_(
                        FreeDate.date > now.date(),  # Якщо дата більша за сьогоднішню, запис активний
                        and_(
                            FreeDate.date == now.date(),  # Якщо це сьогоднішня дата, перевіряємо час
                            Notes.time > now.time(),
                        ),
                    )
                )
            )
            return result.scalars().all()

    @staticmethod
    async def get_active_notes_by_user_id(user_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Notes).join(FreeDate, FreeDate.id == Notes.date_id)
            .filter(Notes.user_id == user_id,
                or_(
                    FreeDate.date
                    > now.date(),  # Якщо дата більша за сьогоднішню, запис активний
                    and_(
                        FreeDate.date
                        == now.date(),  # Якщо це сьогоднішня дата, перевіряємо час
                        Notes.time > now.time(),
                    ),
                ),
            )
        )
            return result.scalars().all()

    @staticmethod
    async def get_active_notes_by_note_id(note_id: int):
        async with async_session() as session:
            result = await (
            session.execute(select(Notes)
            .join(FreeDate, FreeDate.id == Notes.date_id)
            .filter(
                Notes.id == note_id,
                or_(
                    FreeDate.date
                    > now.date(),  # Якщо дата більша за сьогоднішню, запис активний
                    and_(
                        FreeDate.date
                        == now.date(),  # Якщо це сьогоднішня дата, перевіряємо час
                        Notes.time > now.time(),
                    ),
                ),
            )
        ))
            return result.scalar()


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
        async with async_session() as session:
            result = await session.execute(select(Notes).filter_by(id=note_id))
            note = result.scalar()
            if note:
                note.reminder_hours = reminder_hours
                await session.commit()
