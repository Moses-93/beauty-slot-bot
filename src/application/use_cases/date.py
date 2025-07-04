from datetime import datetime
from typing import List

from src.domain.repositories.abstract_time_slot_repository import (
    AbstractTimeSlotRepository,
)
from src.domain.entities.time import TimeSlot
from src.domain.enums.time_slot import TimeSlotStatus
from src.application.dto.time import TimeSlotDTO
from src.shared.dto.result import ResultDTO
from src.infrastructure.celery.tasks.deactivation.date import deactivate


class CreateTimeSlotUseCase:
    def __init__(self, time_slot_repo: AbstractTimeSlotRepository):
        self._time_slot_repo = time_slot_repo

    async def __call__(self, time_slot_dto: TimeSlotDTO) -> ResultDTO[TimeSlot]:

        time_slot = TimeSlot(
            master_id=time_slot_dto.master_id,
            date=time_slot_dto.date,
            start=time_slot_dto.start,
            end=time_slot_dto.end,
            status=TimeSlotStatus.AVAILABLE,
        )

        created_time_slot = await self._time_slot_repo.create(time_slot)

        if created_time_slot is None:
            return ResultDTO.fail()
        deactivate.apply_async(
            args=[created_time_slot.id],
            eta=datetime.combine(created_time_slot.date, created_time_slot.start),
        )
        return ResultDTO.success(created_time_slot)


class CancelTimeSlotUseCase:
    def __init__(self, time_slot_repo: AbstractTimeSlotRepository):
        self._time_slot_repo = time_slot_repo

    async def __call__(self, id: int) -> ResultDTO:
        result = await self._time_slot_repo.update(id, status=TimeSlotStatus.CANCELLED)

        if result is False:
            return ResultDTO.fail()
        return ResultDTO.success()


class DeleteTimeSlotUseCase:
    def __init__(self, time_slot_repo: AbstractTimeSlotRepository):
        self._time_slot_repo = time_slot_repo

    async def __call__(self, id: int) -> ResultDTO:
        result = await self._time_slot_repo.delete(id)

        if result is False:
            return ResultDTO.fail()
        return ResultDTO.success()


class GetAvailableTimeSlotUseCase:
    def __init__(self, time_slot_repo: AbstractTimeSlotRepository):
        self._time_slot_repo = time_slot_repo

    async def __call__(
        self, master_id: int, limit: int, offset: int
    ) -> ResultDTO[List[TimeSlot]]:
        time_slots = await self._time_slot_repo.get_active_slots(
            master_id, limit, offset
        )
        if time_slots is None:
            return ResultDTO.fail()
        return ResultDTO.success(time_slots)
