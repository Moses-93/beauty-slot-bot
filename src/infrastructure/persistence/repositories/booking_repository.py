from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.abstract_booking_repository import (
    AbstractBookingRepository,
)
from src.domain.entities import booking, time
from src.infrastructure.persistence.models import BookingModel, DateModel
from .base_repository import BaseRepository


class BookingRepository(AbstractBookingRepository):
    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        self._base_repo = BaseRepository(factory_session, BookingModel)

    async def get_bookings(
        self, is_active: bool, limit: int, offset: int
    ) -> Optional[List[booking.Booking]]:
        """Get all bookings."""
        query = (
            select(BookingModel)
            .filter(BookingModel.is_active == is_active)
            .order_by(BookingModel.date.has(DateModel.date))
            .options(
                selectinload(BookingModel.service, BookingModel.date, BookingModel.user)
            )
            .limit(limit)
            .offset(offset)
        )
        result = await self._base_repo.read(query)
        if not result:
            return None
        return [
            booking.Booking(
                id=book.id,
                user_id=book.user_id,
                service_id=book.service_id,
                date_id=book.date_id,
                time=book.time,
                reminder_time=book.reminder_time,
                is_active=book.is_active,
            )
            for book in result
        ]

    async def get_bookings_by_user_id(
        self, user_id: int, is_active: bool, limit: int, offset: int
    ) -> Optional[List[booking.Booking]]:
        """Get bookings by user ID."""
        query = (
            (
                select(BookingModel)
                .filter(
                    BookingModel.user_id == user_id, BookingModel.is_active == is_active
                )
                .order_by(BookingModel.date.has(DateModel.date))
                .options(
                    selectinload(
                        BookingModel.service, BookingModel.date, BookingModel.user
                    )
                )
            )
            .limit(limit)
            .offset(offset)
        )
        result = await self._base_repo.read(query)
        if not result:
            return None
        return [
            booking.Booking(
                id=book.id,
                user_id=book.user_id,
                service_id=book.service_id,
                date_id=book.date_id,
                time=book.time,
                reminder_time=book.reminder_time,
                is_active=book.is_active,
            )
            for book in result
        ]

    async def get_booking_by_id(self, booking_id: int) -> Optional[booking.Booking]:
        """Get a booking by its ID."""
        result = await self._base_repo.read_by_id(booking_id)
        if not result:
            return None
        return booking.Booking(
            id=result.id,
            user_id=result.user_id,
            service_id=result.service_id,
            date_id=result.date_id,
            time=result.time,
            reminder_time=result.reminder_time,
            is_active=result.is_active,
        )

    async def get_busy_slots(
        self,
        date_id: int,
    ) -> List[time.TimeSlot]:
        """Get busy slots for a specific date."""
        query = (
            select(BookingModel)
            .filter(
                BookingModel.date_id == date_id,
                BookingModel.is_active == True,
            )
            .order_by(BookingModel.time)
            .options(selectinload(BookingModel.service))
        )
        result = await self._base_repo.read(query)
        if not result:
            return None
        return [
            time.TimeSlot.create_with_duration(slot.time, slot.service.duration)
            for slot in result
        ]

    async def create(self, booking: booking.Booking) -> Optional[booking.Booking]:
        """Create a new booking."""
        created_book = await self._base_repo.create(booking.to_dict())
        if not created_book:
            return None
        return booking.Booking(
            id=created_book.id,
            user_id=created_book.user_id,
            service_id=created_book.service_id,
            date_id=created_book.date_id,
            time=created_book.time,
            reminder_time=created_book.reminder_time,
            is_active=created_book.is_active,
        )

    async def update(self, booking_id: int, **kwargs) -> bool:
        """Update an existing booking."""
        query = (
            update(BookingModel).where(BookingModel.id == booking_id).values(**kwargs)
        )
        result = await self._base_repo.update(query)
        return result

    async def delete(self, booking_id: int) -> bool:
        """Delete a booking."""
        query = delete(BookingModel).where(BookingModel.id == booking_id)
        result = await self._base_repo.delete(query)
        return result
