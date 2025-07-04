from datetime import date, time, datetime

from src.domain.entities.user import User
from src.domain.entities.booking import Booking
from src.domain.repositories.abstract_booking_repository import (
    AbstractBookingRepository,
)
from src.application.services.booking_factory import BookingFactory
from src.shared.dto.result import ResultDTO
from src.application.dto.booking import BookingDTO
from src.infrastructure.celery.tasks.deactivation.booking import deactivate


class CreateBookingUseCase:
    def __init__(
        self, booking_repo: AbstractBookingRepository, booking_factory: BookingFactory
    ):
        self._booking_repo = booking_repo
        self._booking_factory = booking_factory

    def _schedule_deactivation(booking_id: int, date: date, time: time) -> None:
        """
        Schedule a deactivation task for the booking.
        """
        deactivation_time = datetime.combine(date, time)
        deactivate.apply_async(
            args=[booking_id],
            eta=deactivation_time,
        )

    async def __call__(self, booking_dto: BookingDTO) -> ResultDTO[Booking]:
        """
        Execute the use case to create a booking.
        """
        result = await self._booking_factory.create(booking_dto)
        if not result.is_success:
            return ResultDTO.fail()  # TODO: Add error message return

        booking = result.data

        try:
            booking.confirm()
        except ValueError as e:  # TODO: Replace with custom exception
            return ResultDTO.fail(
                error=str(e), message="..."
            )  # TODO: Add custom error message

        created_booking = await self._booking_repo.create(result.data)

        if not created_booking:
            return ResultDTO.fail()

        if created_booking.should_schedule_reminder(datetime.now()):
            self._schedule_deactivation(
                created_booking.id,
                created_booking.time_slot.date,
                created_booking.time_slot.start,
            )
        return ResultDTO.success(created_booking)


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
