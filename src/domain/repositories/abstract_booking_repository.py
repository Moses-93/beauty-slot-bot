from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.booking import Booking


class AbstractBookingRepository(ABC):

    @abstractmethod
    async def get_master_bookings(
        self, is_active: bool, master_id: int, limit: int = 10, offset: int = 0
    ) -> Optional[List[Booking]]:
        """Get bookings for a specific master."""
        pass

    @abstractmethod
    async def get_client_bookings(
        self, is_active: bool, client_id: int, limit: int = 10, offset: int = 0
    ) -> Optional[List[Booking]]:
        """Get bookings for a specific client."""
        pass

    @abstractmethod
    async def get_booking_by_id(self, booking_id: int) -> Optional[Booking]:
        """Get a booking by its ID."""
        pass

    @abstractmethod
    async def create(self, book: Booking) -> Optional[Booking]:
        """Create a new booking."""
        pass

    @abstractmethod
    async def update(self, booking_id: int, **kwargs) -> bool:
        """Update an existing booking."""
        pass

    @abstractmethod
    async def delete(self, booking_id: int) -> bool:
        """Delete a booking."""
        pass
