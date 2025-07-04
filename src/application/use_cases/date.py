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

    async def __call__(self, time_slot_dto: TimeSlotDTO) -> ResultDTO[TimeSlot]:
        created_time_slot = await self._time_slot_repo.create(time_slot_dto)

        if created_time_slot is None:
            return ResultDTO.fail()
        deactivate.apply_async(
            args=[created_time_slot.id],
            eta=datetime.combine(created_time_slot.date, created_time_slot.start),
        )
        return ResultDTO.success(created_time_slot)


class DeactivateDateUseCase:
    def __init__(self, time_slot_repo: AbstractTimeSlotRepository):
        self._time_slot_repo = time_slot_repo

    async def __call__(self, id: int, *args, **kwds) -> ResultDTO:
        result = await self._repo.update(id, is_active=False)

        if result is False:
            return ResultDTO.fail()
        return ResultDTO.success()


class DeleteDateUseCase:
    def __init__(self, time_slot_repo: AbstractTimeSlotRepository):
        self._time_slot_repo = time_slot_repo

    async def __call__(self, id: int, *args, **kwds) -> ResultDTO:
        result = await self._repo.delete(id)

        if result is False:
            return ResultDTO.fail()
        return ResultDTO.success()


class GetAvailableDateUseCase:
    def __init__(self, time_slot_repo: AbstractTimeSlotRepository):
        self._time_slot_repo = time_slot_repo

    async def __call__(self, limit: int, offset: int) -> ResultDTO[List[DateDTO]]:
        dates = await self._repo.get_active_dates(limit, offset)
        if dates is None:
            return ResultDTO.fail()
        return ResultDTO.success(dates)
