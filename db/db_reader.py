from datetime import datetime
from .repository import (
    NotesRepository,
    ServiceRepository,
    FreeDateRepository,

)

class GetService:
    def __init__(self, service_id=None, name=None, all_services=False):
        self.service_id = service_id
        self.name = name
        self.all_services = all_services
        self.services = None

    async def initialize(self):
        if self.service_id:
            self.services = await ServiceRepository.get_service_by_id(self.service_id)
        elif self.name:
            self.services = await ServiceRepository.get_service_by_name(self.name)
        elif self.all_services:
            self.services = await ServiceRepository.get_all_services()

    async def get(self):
        await self.initialize()
        return self.services
    
    async def get_name(self):
        await self.initialize()
        return self.services.name if self.services else None


class GetFreeDate:
    def __init__(self, date_id=None, date=None, all_dates=False):
        self.date_id = date_id
        self.date = date
        self.all_dates = all_dates
        self.free_date = None

    async def initialize(self):
        if self.date_id:
            self.free_date = await FreeDateRepository().get_free_dates_by_date_id(
                self.date_id
            )
        elif self.date:
            self.free_date = await FreeDateRepository().get_free_date_by_date(self.date)
        elif self.all_dates:
            now = datetime.now()
            self.free_date = await FreeDateRepository().get_all_free_dates(now)
        else:
            self.free_date = None

    async def get(self):
        await self.initialize()
        return self.free_date

    @property
    async def get_date(self):
        await self.initialize()
        return self.free_date.date if self.free_date else None


class GetNotes:
    def __init__(self, user_id=None, date_id=None, note_id=None, only_active=False):
        self.user_id = user_id
        self.date_id = date_id
        self.note_id = note_id
        self.only_active = only_active

    async def initialize(self):
        now = datetime.now()
        if self.user_id:
            if self.only_active:
                self.notes = await NotesRepository().get_active_notes_by_user_id(
                    self.user_id, now
                )
            else:
                self.notes = await NotesRepository().get_notes_by_user_id(self.user_id)
        elif self.date_id:
            self.notes = await NotesRepository().get_notes_by_date_id(self.date_id)
        elif self.note_id:
            self.notes = await NotesRepository().get_active_notes_by_note_id(
                self.note_id, now
            )
        elif self.only_active:
            self.notes = await NotesRepository().get_all_active_notes(now)

    async def get_notes(self):
        await self.initialize()
        return self.notes
