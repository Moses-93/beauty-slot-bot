from .repository import NotesRepository, ServiceRepository, FreeDateRepository


class GetService:
    def __init__(self, service_id=None):
        if service_id:
            self.service = ServiceRepository().get_service_by_id(service_id)
        else:
            self.service = None

    def get_all_services(self):
        return ServiceRepository.get_all_services()

    @property
    def id(self):
        return self.service.id

    @property
    def name(self):
        return self.service.name

    @property
    def price(self):
        return self.service.price

    @property
    def durations(self):
        return self.service.durations


class GetFreeDate:
    def __init__(self, date_id=None):
        if date_id:
            self.free_date = FreeDateRepository().get_free_dates_by_service_id(date_id)
        else:
            self.free_date = None

    def get_all_free_dates(self):
        return FreeDateRepository.get_all_free_dates()

    @property
    def id(self):
        return self.free_date.id

    @property
    def date(self):
        return self.free_date.date

    @property
    def free(self):
        return self.free_date.free

    @property
    def now(self):
        return self.free_date.now


class GetNotes:
    def __init__(self, user_id=None, date_id=None):
        if user_id:
            self.notes = NotesRepository().get_notes_by_user_id(user_id)
        elif date_id:
            self.notes = NotesRepository().get_notes_by_date_id(date_id)
        else:
            self.notes = None

    def get_all_notes(self):
        return self.notes
