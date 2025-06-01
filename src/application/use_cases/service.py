from typing import List
from src.domain.repositories.abstract_service_repository import (
    AbstractServiceRepository,
)
from src.application.dto.service import ServiceDTO
from src.shared.dto.result import ResultDTO


class CreateServiceUseCase:
    def __init__(self, service_repo: AbstractServiceRepository):
        self._repo = service_repo

    async def __call__(self, dto: ServiceDTO, *args, **kwds) -> ResultDTO[ServiceDTO]:
        created_service = await self._repo.create(dto)

        if created_service is None:
            return ResultDTO.fail()
        return ResultDTO.success(created_service)


class EditServiceUseCase:
    def __init__(self, service_repo: AbstractServiceRepository):
        self._repo = service_repo

    async def __call__(self, service_id: int, *args, **kwds) -> ResultDTO[ServiceDTO]:
        result = await self._repo.update(service_id, **kwds)

        if result is False:
            return ResultDTO.fail()
        updated_service = await self._repo.get_by_id(service_id)
        return ResultDTO.success(updated_service)


class GetServicesUseCase:
    def __init__(self, service_repo: AbstractServiceRepository):
        self._repo = service_repo

    async def __call__(self, *args, **kwds) -> ResultDTO[List[ServiceDTO]]:
        services = await self._repo.get_active()

        if services is not None:
            return ResultDTO.success(services)
        return ResultDTO.fail()
