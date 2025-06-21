from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.booking import Booking
from src.domain.entities.time import TimeSlot


class AbstractBookingRepository(ABC):

    @abstractmethod
    async def get_bookings(
        self, is_active: bool, limit: int, offset: int
    ) -> Optional[List[Booking]]:
        """Get all bookings."""
        pass

    @abstractmethod
    async def get_bookings_by_user_id(
        self, user_id: int, is_active: bool, limit: int, offset: int
    ) -> Optional[List[Booking]]:
        """Get all bookings for a specific user."""
        pass

    @abstractmethod
    async def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        """Get a booking by its ID."""
        pass

    @abstractmethod
    async def get_busy_slots(self, date_id: int) -> Optional[List[TimeSlot]]:
        """Get busy slots for a specific date."""
        pass

    @abstractmethod
    async def create(self, booking_data: Booking) -> Optional[Booking]:
        """Create a new booking."""
        pass

    @abstractmethod
    async def update(self, booking_id: int, **kwargs) -> bool:
        """Update an existing booking."""
        pass

    @abstractmethod
    async def delete(self, booking_id: int) -> bool:
        """Delete a booking by its ID."""
        pass
