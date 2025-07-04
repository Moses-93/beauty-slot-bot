from src.domain.repositories.abstract_contact_repository import (
    AbstractContactRepository,
)
from src.application.dto.contact import ContactDTO
from src.shared.dto.result import ResultDTO


class GetContactsUseCase:
    def __init__(self, contact_repo: AbstractContactRepository):
        self._repo = contact_repo

    async def __call__(self, master_id: int) -> ResultDTO[ContactDTO]:
        contact = await self._repo.get(
            master_id
        )  # TODO: Add try/except for error handling and logging
        if contact:
            return ResultDTO.success(contact)
        return ResultDTO.fail()
