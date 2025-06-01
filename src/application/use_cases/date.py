from typing import List

from src.domain.repositories.abstract_date_repository import AbstractDateRepository
from application.services.date_scheduler import DeactivationScheduler
from src.application.dto.date import DateDTO
from src.shared.dto.result import ResultDTO


class CreateDateUseCase:
    def __init__(
        self, date_repo: AbstractDateRepository, scheduler: DeactivationScheduler
    ):
        self._repo = date_repo
        self._scheduler = scheduler

    async def __call__(self, date_dto: DateDTO, *args, **kwds) -> ResultDTO[DateDTO]:
        created_date = await self._repo.create(date_dto)

        if created_date is None:
            return ResultDTO.fail()
        self._scheduler.schedule(created_date.id, created_date.deactivation_time)
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

    async def __call__(self, *args, **kwds) -> ResultDTO[List[DateDTO]]:
        dates = await self._repo.get_active_dates()
        if dates is None:
            return ResultDTO.fail()
        return ResultDTO.success(dates)
