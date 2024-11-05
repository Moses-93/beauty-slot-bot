from .repository import (
    NotesRepository,
    ServiceRepository,
    FreeDateRepository,
    NotesDeleteRepository,
    UpdateNotesRepository,
)

from utils.format_datetime import NowDatetime


class GetService:
    def __init__(self, service_id=None, name=None):
        self.service_id = service_id
        self.name = name
        self.service = None

    async def initialize(self):
        if self.service_id:
            self.service = await ServiceRepository.get_service_by_id(self.service_id)
        elif self.name:
            self.service = await ServiceRepository.get_service_by_name(self.name)

    async def get(self):
        await self.initialize()
        return self.service

    async def get_all_services(self):
        return await ServiceRepository.get_all_services()

    async def get_id(self):
        return self.service.id if self.service else None

    async def get_name(self):
        return self.service.name if self.service else None

    async def get_price(self):
        return self.service.price if self.service else None

    async def get_durations(self):
        return self.service.durations if self.service else None


class GetFreeDate:
    def __init__(self, date_id=None, date=None):
        self.date_id = date_id
        self.date = date
        self.free_date = None

    async def initialize(self):
        if self.date_id:
            self.free_date = await FreeDateRepository().get_free_dates_by_date_id(
                self.date_id
            )
        elif self.date:
            self.free_date = await FreeDateRepository().get_free_date_by_date(self.date)
        else:
            self.free_date = None

    async def get(self):
        await self.initialize()
        return self.free_date

    async def get_all_free_dates(self):
        return await FreeDateRepository().get_all_free_dates()

    @property
    def id(self):
        return self.free_date.id

    @property
    def get_date(self):
        return self.free_date.date

    @property
    def get_free(self):
        return self.free_date.free

    @property
    def get_now(self):
        return self.free_date.now


class GetNotes:
    def __init__(self, user_id=None, date_id=None, note_id=None, only_active=False):
        self.user_id = user_id
        self.date_id = date_id
        self.note_id = note_id
        self.only_active = only_active

    async def initialize(self):
        if self.user_id:
            if self.only_active:
                self.notes = await NotesRepository().get_active_notes_by_user_id(
                    self.user_id
                )
            else:
                self.notes = await NotesRepository().get_notes_by_user_id(self.user_id)
        elif self.date_id:
            self.notes = await NotesRepository().get_notes_by_date_id(self.date_id)
        elif self.note_id:
            self.notes = await NotesRepository().get_active_notes_by_note_id(
                self.note_id
            )
        elif self.only_active:
            self.notes = await NotesRepository().get_all_active_notes()

    async def get_all_notes(self):
        await self.initialize()
        return self.notes


class DeleteNotes:
    def __init__(self, note_id: int):
        self.note_id = note_id

    async def delete_note(self):
        await NotesDeleteRepository().delete_notes_by_note_id(self.note_id)


class UpdateNotes:
    def __init__(self, note_id: int, reminder_hours: int) -> None:
        self.note_id = note_id
        self.reminder_hours = reminder_hours

    async def update_reminder(self) -> None:
        await UpdateNotesRepository().update_reminder(self.note_id, self.reminder_hours)
