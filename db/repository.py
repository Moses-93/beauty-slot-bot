from .models import Service, FreeDate, Notes, session
from datetime import datetime


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
            FreeDate.free.is_(True), FreeDate.now > datetime.now()
        )


class NotesRepository:

    @staticmethod
    def get_notes_by_user_id(user_id):
        return session.query(Notes).filter_by(user_id=user_id).all()

    @staticmethod
    def get_notes_by_date_id(date_id):
        return session.query(Notes).filter_by(date_id=date_id).all()
