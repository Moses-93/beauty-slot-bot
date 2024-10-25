from sqlalchemy import and_, or_
from .models import Service, FreeDate, Notes, session
from utils.format_datetime import NowDatetime, FormatTime

now = NowDatetime().now_datetime()
format_time = FormatTime()


class ServiceRepository:

    @staticmethod
    def get_service_by_id(service_id):
        return session.query(Service).get(service_id)

    def get_all_services():
        return session.query(Service).all()


class FreeDateRepository:

    @staticmethod
    def get_free_dates_by_service_id(date_id):
        return session.query(FreeDate).get(date_id)

    @staticmethod
    def get_all_free_dates():
        return session.query(FreeDate).filter(
            FreeDate.free.is_(True), FreeDate.now > now
        )


class NotesRepository:

    @staticmethod
    def get_notes_by_user_id(user_id: int):
        return session.query(Notes).filter_by(user_id=user_id).all()

    @staticmethod
    def get_notes_by_date_id(date_id: int):
        return session.query(Notes).filter_by(date_id=date_id).all()

    @staticmethod
    def get_all_active_notes():
        return (
            session.query(Notes)
            .join(FreeDate, FreeDate.id == Notes.date_id)
            .filter(
                or_(
                    FreeDate.date
                    > now.date(),  # Якщо дата більша за сьогоднішню, запис активний
                    and_(
                        FreeDate.date
                        == now.date(),  # Якщо це сьогоднішня дата, перевіряємо час
                        Notes.time > now.time(),
                    ),
                )
            )
            .all()
        )

    @staticmethod
    def get_active_notes_by_user_id(user_id: int):
        return (
            session.query(Notes)
            .join(FreeDate, FreeDate.id == Notes.date_id)
            .filter(
                Notes.user_id == user_id,
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
            .all()
        )

    @staticmethod
    def get_active_notes_by_note_id(note_id: int):
        return (
            session.query(Notes)
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
            .first()
        )


class NotesDeleteRepository:

    @staticmethod
    def delete_notes_by_note_id(note_id: int):
        session.query(Notes).filter_by(id=note_id).delete()
        session.commit()


class UpdateNotesRepository:

    @staticmethod
    def update_reminder(note_id, reminder_hours: int):
        note = session.query(Notes).filter_by(id=note_id).first()
        note.reminder_hours = reminder_hours
        session.commit()
