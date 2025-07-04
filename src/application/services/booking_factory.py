from src.domain.entities.booking import Booking
from src.application.dto.booking import BookingDTO
from src.shared.dto.result import ResultDTO
from src.domain.repositories.abstract_service_repository import (
    AbstractServiceRepository,
)
from src.domain.repositories.abstract_time_slot_repository import (
    AbstractTimeSlotRepository,
)


class BookingFactory:
    def __init__(
        self,
        time_slot_repo: AbstractTimeSlotRepository,
        service_repo: AbstractServiceRepository,
    ):
        self._time_slot_repo = time_slot_repo
        self._service_repo = service_repo

    async def create(self, book_dto: BookingDTO) -> ResultDTO[Booking]:
        """
        Create a new booking instance.
        """
        service = await self._service_repo.get_by_id(book_dto.service_id)
        if not service:
            return ResultDTO.fail(
                error="SERVICE_NOT_FOUND"
            )  # TODO: Add enum for errors

        time_slot = await self._time_slot_repo.get_slot_by_id(book_dto.time_slot_id)
        if not time_slot:
            return ResultDTO.fail(
                error="TIME_SLOT_NOT_FOUND"
            )  # TODO: Add enum for errors
        return ResultDTO.success(
            Booking(
                master_id=book_dto.master_id,
                client_id=book_dto.client_id,
                service=service,
                time_slot=time_slot,
                reminder_time=book_dto.reminder_time,
                is_active=True,
            )
        )
