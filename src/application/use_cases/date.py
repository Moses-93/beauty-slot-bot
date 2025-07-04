from datetime import datetime
from typing import List

from src.domain.repositories.abstract_time_slot_repository import (
    AbstractTimeSlotRepository,
)
from src.domain.entities.time import TimeSlot
from src.infrastructure.celery.tasks.deactivation.date import deactivate
from src.application.dto.time import TimeSlotDTO
from src.shared.dto.result import ResultDTO


class CreateTimeSlotUseCase:
    def __init__(self, time_slot_repo: AbstractTimeSlotRepository):
        self._time_slot_repo = time_slot_repo

    async def __call__(self, date_dto: DateDTO, *args, **kwds) -> ResultDTO[DateDTO]:
        created_date = await self._repo.create(date_dto)

        if created_date is None:
            return ResultDTO.fail()
        deactivate.apply_async(
            args=[created_date.id],
            eta=created_date.deactivation_time,
        )
        return ResultDTO.success(
            DateDTO(
                id=created_date.id,
                date=created_date.date,
                deactivation_time=created_date.deactivation_time,
                is_active=created_date.is_active,
            )
        )


class DeactivateDateUseCase:
    def __init__(self, date_repo: AbstractDateRepository):
        self._repo = date_repo

    async def __call__(self, id: int, *args, **kwds) -> ResultDTO:
        result = await self._repo.update(id, is_active=False)

        if result is False:
            return ResultDTO.fail()
        return ResultDTO.success()


class DeleteDateUseCase:
    def __init__(self, date_repo: AbstractDateRepository):
        self._repo = date_repo

    async def __call__(self, id: int, *args, **kwds) -> ResultDTO:
        result = await self._repo.delete(id)

        if result is False:
            return ResultDTO.fail()
        return ResultDTO.success()


class GetAvailableDateUseCase:
    def __init__(self, date_repo: AbstractDateRepository):
        self._repo = date_repo

    async def __call__(self, limit: int, offset: int) -> ResultDTO[List[DateDTO]]:
        dates = await self._repo.get_active_dates(limit, offset)
        if dates is None:
            return ResultDTO.fail()
        return ResultDTO.success(dates)
