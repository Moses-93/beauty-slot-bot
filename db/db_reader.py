from datetime import datetime
import logging
from .repository import (
    NotesRepository,
    ServiceRepository,
    FreeDateRepository,

)
logger = logging.getLogger(__name__)

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
    def __init__(self, date_id=None, date=None, free_dates=False, all_dates=False):
        self.date_id = date_id
        self.date = date
        self.free_dates = free_dates
        self.all_dates = all_dates
        self.now = datetime.now()
        self.free_date = None
        logger.info(f"NOW DATE(in GetFreeDate): {self.now}")

    async def initialize(self):
        if self.date_id:
            self.free_date = await FreeDateRepository().get_free_dates_by_date_id(
                self.date_id
            )
        elif self.date:
            self.free_date = await FreeDateRepository().get_free_date_by_date(self.date)
        elif self.free_dates:
            self.free_date = await FreeDateRepository().get_all_free_dates(self.now)
        elif self.all_dates:
            self.free_date = await FreeDateRepository().get_dates_last_30_days(self.now)
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
    def __init__(self, user_id:int=None, date_id:int=None, note_id:int=None, day_filter:int=None, only_active=False):
        self.user_id = user_id
        self.date_id = date_id
        self.note_id = note_id
        self.day_filter = day_filter
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
        elif self.day_filter:
            self.notes = await NotesRepository().get_notes_by_days(self.day_filter)


    async def get_notes(self):
        await self.initialize()
        return self.notes
