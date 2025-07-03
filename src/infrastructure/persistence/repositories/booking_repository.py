from typing import List, Optional
from sqlalchemy import select, update, delete, Select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.abstract_booking_repository import (
    AbstractBookingRepository,
)
from src.domain.entities.booking import Booking
from src.domain.entities.time import TimeSlot
from src.domain.entities.service import Service
from src.infrastructure.persistence.models import BookingModel
from .base_repository import BaseRepository


class BookingRepository(AbstractBookingRepository):  # TODO: Add custom exceptions
    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        self._base_repo = BaseRepository(factory_session, BookingModel)

    async def _get_bookings(
        self,
        is_active: bool,
        limit: int,
        offset: int,
        master_id: int | None = None,
        client_id: int | None = None,
    ) -> Optional[List[Booking]]:
        query = select(BookingModel).options(
            selectinload(BookingModel.service), selectinload(BookingModel.time_slot)
        )
        query = self._apply_filters(query, is_active, master_id, client_id)
        query = query.order_by(BookingModel.created_at).limit(limit).offset(offset)
        result = await self._base_repo.read(query)
        if not result:
            return None

        return [self._to_entity(book) for book in result]

    async def get_master_bookings(
        self, is_active: bool, master_id: int, limit: int = 10, offset: int = 0
    ) -> Optional[List[Booking]]:
        """Get bookings for a specific master."""
        return await self._get_bookings(is_active, limit, offset, master_id=master_id)

    async def get_client_bookings(
        self, is_active: bool, client_id: int, limit: int = 10, offset: int = 0
    ) -> Optional[List[Booking]]:
        """Get bookings for a specific client."""
        return await self._get_bookings(is_active, limit, offset, client_id=client_id)

    async def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        """Get a booking by its ID."""
        booking = await self._base_repo.read_by_id(booking_id)
        if not booking:
            return None
        return self._to_entity(booking)

    async def create(self, book: Booking) -> Optional[Booking]:
        """Create a new booking."""
        created_book = await self._base_repo.create(self._to_model(book))
        if not created_book:
            return None
        return self._to_entity(created_book)

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

    def _to_entity(self, model: BookingModel) -> Booking:
        """Convert BookingModel to Booking entity."""
        return Booking(
            id=model.id,
            client_id=model.client_id,
            master_id=model.master_id,
            service=Service(
                id=model.service_id,
                title=model.service.title,
                price=model.service.price,
                duration=model.service.duration,
            ),
            time_slot=TimeSlot(
                id=model.time_slot.id,
                master_id=model.time_slot.master_id,
                date=model.time_slot.date,
                start=model.time_slot.start_time,
                end=model.time_slot.end_time,
                is_active=model.time_slot.is_active,
                is_booked=model.time_slot.is_booked,
            ),
            reminder_time=model.reminder_time,
            is_active=model.is_active,
        )

    def _to_model(self, entity: Booking) -> BookingModel:
        """Convert Booking entity to BookingModel."""
        return BookingModel(
            id=entity.id,
            client_id=entity.client_id,
            master_id=entity.master_id,
            service_id=entity.service.id,
            time_slot_id=entity.time_slot.id,
            reminder_time=entity.reminder_time,
            is_active=entity.is_active,
        )

    def _apply_filters(
        self,
        query: Select,
        is_active: bool,
        master_id: Optional[int] = None,
        client_id: Optional[int] = None,
    ) -> Select:
        """Apply filters to the query based on the parameters."""
        query = query.filter(BookingModel.is_active == is_active)
        if master_id is not None:
            query = query.filter(BookingModel.master_id == master_id)
        if client_id is not None:
            query = query.filter(BookingModel.client_id == client_id)
        return query
