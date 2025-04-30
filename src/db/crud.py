from datetime import datetime
from aiocache import cached
from .config import Session
from .models import Booking, Service, Date, Admin
from .repository import ImplementationCRUD
from src.decorators.cache_tools import cache_note_id


class NotesManager:

    def __init__(self, notes: ImplementationCRUD):
        self.notes = notes

    @cache_note_id
    async def create(self, **kwargs):
        result = await self.notes.create(Booking, **kwargs)
        if result:
            return result

    async def read(self, relations: tuple = None, expressions: tuple = None, **filters):
        if filters.get("active"):
            now = datetime.now()
            expressions = (
                Booking.date.has(Date.date >= now.date()),
                Booking.time > now.time(),
            )
        result = await self.notes.read(
            Booking, relations=relations, expressions=expressions, **filters
        )
        return result

    async def update(self, *expressions, **filters):
        await self.notes.update(Booking, *expressions, **filters)

    async def delete(self, **kwargs):
        await self.notes.delete(Booking, **kwargs)


class ServicesManager:

    def __init__(self, services: ImplementationCRUD):
        self.services = services

    async def create(self, **kwargs):
        await self.services.create(Service, **kwargs)

    @cached(ttl=7200, alias="queries_cache")
    async def read(self, expressions: tuple = None, **filters):
        result = await self.services.read(Service, expressions=expressions, **filters)
        return result

    async def update(self, *expressions, **filters):
        await self.services.update(Service, *expressions, **filters)

    async def delete(self, **kwargs):
        await self.services.delete(Service, **kwargs)


class DatesManager:

    def __init__(self, dates: ImplementationCRUD):
        self.dates = dates

    async def create(self, **kwargs):
        await self.dates.create(Date, **kwargs)

    @cached(ttl=7200, alias="queries_cache")
    async def read(self, expressions: tuple = None, **filters):
        if filters.get("is_active"):
            now = datetime.now()
            expressions = (Date.deactivation_time > now,)
        result = await self.dates.read(Date, expressions=expressions, **filters)
        return result

    async def update(self, *expressions, **filters):
        await self.dates.update(Date, *expressions, **filters)

    async def delete(self, **kwargs):
        await self.dates.delete(Date, **kwargs)


class AdminsManager:

    def __init__(self, admins: ImplementationCRUD):
        self.admins = admins

    async def create(self, **kwargs):
        await self.admins.create(Admin, **kwargs)

    @cached(ttl=1800, alias="queries_cache")
    async def read(self, expressions: list = None, **filters):
        result = await self.admins.read(Admin, expressions=expressions, **filters)
        return result

    async def update(self, *expressions, **filters):
        await self.admins.update(Admin, *expressions, **filters)

    async def delete(self, *expressions):
        await self.admins.delete(Admin, *expressions)


base_crud = ImplementationCRUD(session=Session)
notes_manager = NotesManager(notes=base_crud)
services_manager = ServicesManager(services=base_crud)
dates_manager = DatesManager(dates=base_crud)
admins_manager = AdminsManager(admins=base_crud)
