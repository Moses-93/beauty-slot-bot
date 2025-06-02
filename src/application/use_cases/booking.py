from src.domain.entities.booking import Booking
from src.domain.repositories.abstract_booking_repository import (
    AbstractBookingRepository,
)
from src.shared.dto.result import ResultDTO
from src.application.dto.booking import BookingDTO


class CreateBookingUseCase:
    def __init__(self, booking_repo: AbstractBookingRepository):
        self._booking_repo = booking_repo

    async def __call__(
        self, booking_dto: BookingDTO, *args, **kwds
    ) -> ResultDTO[Booking]:
        """
        Execute the use case to create a booking.
        """
        booking = Booking(booking_dto.model_dump())

        created_booking = await self._booking_repo.create(booking)

        if created_booking:
            return ResultDTO.success(created_booking)

        return ResultDTO.fail()
