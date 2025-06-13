from src.domain.repositories.abstract_contact_repository import (
    AbstractContactRepository,
)
from src.application.dto.contact import ContactDTO
from src.shared.dto.result import ResultDTO


class GetContactsUseCase:
    def __init__(self, contact_repo: AbstractContactRepository):
        self._repo = contact_repo

    async def __call__(self, *args, **kwds) -> ResultDTO[ContactDTO]:
        contacts = (
            await self._repo.get()
        )  # TODO: Add try/except for error handling and logging
        if contacts:
            return ResultDTO.success(contacts)
        return ResultDTO.fail()
