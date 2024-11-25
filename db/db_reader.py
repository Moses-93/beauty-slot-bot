from .repository import (
    BaseGetNotes,
    BaseGetServices,
    BaseGetDates,
    base_get_notes,
    base_get_service,
    base_get_free_date,
)


class GetNotes:

    def __init__(self, notes: BaseGetNotes):
        self.notes = notes

    async def get_notes(self, *expressions, **filters):
        result = await self.notes.get_notes(*expressions, **filters)
        return result


class GetServices:

    def __init__(self, services: BaseGetServices):
        self.services = services

    async def get_service(self, first=False, **filters):
        result = await self.services.get_service(**filters)
        if first and result:
            return result[0]
        return result


class GetDates:

    def __init__(self, dates: BaseGetDates):
        self.dates = dates

    async def get_date(self, first=False, **filters):
        result = await self.dates.get_date(**filters)
        if first and result:
            return result[0]
        return result


get_notes = GetNotes(base_get_notes)
get_service = GetServices(base_get_service)
get_date = GetDates(base_get_free_date)
