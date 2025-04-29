from datetime import datetime
from aiocache import cached
from .config import Session
from .models import Notes, Services, Dates, Admins
from .repository import ImplementationCRUD
from decorators.cache_tools import cache_note_id


class NotesManager:

    def __init__(self, notes: ImplementationCRUD):
        self.notes = notes

    @cache_note_id
    async def create(self, **kwargs):
        result = await self.notes.create(Notes, **kwargs)
        if result:
            return result

    async def read(self, relations: tuple = None, expressions: tuple = None, **filters):
        if filters.get("active"):
            now = datetime.now()
            expressions = (
                Notes.date.has(Dates.date >= now.date()),
                Notes.time > now.time(),
            )
        result = await self.notes.read(
            Notes, relations=relations, expressions=expressions, **filters
        )
        return result

    async def update(self, *expressions, **filters):
        await self.notes.update(Notes, *expressions, **filters)

    async def delete(self, **kwargs):
        await self.notes.delete(Notes, **kwargs)


class ServicesManager:

    def __init__(self, services: ImplementationCRUD):
        self.services = services

    async def create(self, **kwargs):
        await self.services.create(Services, **kwargs)

    @cached(ttl=7200, alias="queries_cache")
    async def read(self, expressions: tuple = None, **filters):
        result = await self.services.read(Services, expressions=expressions, **filters)
        return result

    async def update(self, *expressions, **filters):
        await self.services.update(Services, *expressions, **filters)

    async def delete(self, **kwargs):
        await self.services.delete(Services, **kwargs)


class DatesManager:

    def __init__(self, dates: ImplementationCRUD):
        self.dates = dates

    async def create(self, **kwargs):
        await self.dates.create(Dates, **kwargs)

    @cached(ttl=7200, alias="queries_cache")
    async def read(self, expressions: tuple = None, **filters):
        if filters.get("free"):
            now = datetime.now()
            expressions = (Dates.del_time > now,)
        result = await self.dates.read(Dates, expressions=expressions, **filters)
        return result

    async def update(self, *expressions, **filters):
        await self.dates.update(Dates, *expressions, **filters)

    async def delete(self, **kwargs):
        await self.dates.delete(Dates, **kwargs)


class AdminsManager:

    def __init__(self, admins: ImplementationCRUD):
        self.admins = admins

    async def create(self, **kwargs):
        await self.admins.create(Admins, **kwargs)

    @cached(ttl=1800, alias="queries_cache")
    async def read(self, expressions: list = None, **filters):
        result = await self.admins.read(Admins, expressions=expressions, **filters)
        return result

    async def update(self, *expressions, **filters):
        await self.admins.update(Admins, *expressions, **filters)

    async def delete(self, *expressions):
        await self.admins.delete(Admins, *expressions)


base_crud = ImplementationCRUD(session=Session)
notes_manager = NotesManager(notes=base_crud)
services_manager = ServicesManager(services=base_crud)
dates_manager = DatesManager(dates=base_crud)
admins_manager = AdminsManager(admins=base_crud)
