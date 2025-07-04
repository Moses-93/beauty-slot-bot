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

    async def create(
        self,
        user_id: int,
        service_id: int,
        date_id: str,
        time: time,
        reminder_time: Optional[datetime] = None,
    ) -> ResultDTO[Booking]:
        """
        Create a new booking instance.
        """
        service = await self._service_repo.get_by_id(service_id)
        if not service:
            return ResultDTO.fail(
                error="SERVICE_NOT_FOUND"
            )  # TODO: Add enum for errors

        date = await self._date_repo.get_date_by_id(date_id)
        if not date:
            return ResultDTO.fail(error="DATE_NOT_FOUND")  # TODO: Add enum for errors
        return ResultDTO.success(
            Booking(
                user_id=user_id,
                service=service,
                date=date,
                time=time,
                reminder_time=reminder_time,
            )
        )
