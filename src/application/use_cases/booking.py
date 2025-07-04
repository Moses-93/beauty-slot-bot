from datetime import date, time, datetime

from src.domain.entities.user import User
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

    def _schedule_deactivation(booking_id: int, date: date, time: time) -> None:
        """
        Schedule a deactivation task for the booking.
        """
        deactivation_time = datetime.combine(date, time)
        deactivate.apply_async(
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


class GetBookingUseCase:
    def __init__(self, booking_repo: AbstractBookingRepository):
        self._booking_repo = booking_repo

    async def __call__(
        self,
        user: User,
        is_active: bool,
        limit: int = 5,
        offset: int = 0,
        *args,
        **kwds
    ) -> ResultDTO[Booking]:
        """Execute the use case to get a booking by its status and user."""
        if user.is_client:
            bookings = await self._booking_repo.get_bookings_by_user_id(
                user.id, is_active, limit, offset
            )
        else:
            bookings = await self._booking_repo.get_bookings(is_active, limit, offset)
        return ResultDTO.success(bookings) if bookings else ResultDTO.fail()
