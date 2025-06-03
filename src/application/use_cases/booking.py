from datetime import date, time, datetime
from src.domain.entities.booking import Booking
from src.domain.repositories.abstract_booking_repository import (
    AbstractBookingRepository,
)
from src.shared.dto.result import ResultDTO
from src.application.dto.booking import BookingDTO
from src.infrastructure.celery.tasks.deactivation.booking import deactivate


class CreateBookingUseCase:
    def __init__(self, booking_repo: AbstractBookingRepository):
        self._booking_repo = booking_repo

    async def _schedule_deactivation(booking_id: int, date: date, time: time) -> None:
        """
        Schedule a deactivation task for the booking.
        """
        deactivation_time = datetime.combine(date, time)
        await deactivate.apply_async(
            args=[booking_id],
            eta=deactivation_time,
        )

    async def __call__(
        self, booking_dto: BookingDTO, *args, **kwds
    ) -> ResultDTO[Booking]:
        """
        Execute the use case to create a booking.
        """
        booking = Booking(booking_dto.model_dump())

        created_booking = await self._booking_repo.create(booking)

        if created_booking:
            await self._schedule_deactivation(
                created_booking.id,
                created_booking.date.date,
                created_booking.time,
            )
            return ResultDTO.success(created_booking)

        return ResultDTO.fail()


class DeactivateBookingUseCase:
    def __init__(self, booking_repo: AbstractBookingRepository):
        self._booking_repo = booking_repo

    async def __call__(self, id: int, *args, **kwds) -> ResultDTO:
        """
        Execute the use case to deactivate a booking.
        """
        result = await self._booking_repo.update(id, is_active=False)

        if result:
            return ResultDTO.success()

        return ResultDTO.fail()
