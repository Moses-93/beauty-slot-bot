from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.time import TimeSlot


class AbstractTimeSlotRepository(ABC):
    @abstractmethod
    async def get_active_slots(
        self, master_id: int, limit: int, offset: int
    ) -> Optional[List[TimeSlot]]:
        """Get active time slots."""
        pass

    @abstractmethod
    async def get_slot_by_id(self, slot_id: int) -> Optional[TimeSlot]:
        """Get a time slot by its ID."""
        pass

    @abstractmethod
    async def mark_as_booked(self, slot_id: int) -> bool:
        """Mark a time slot as booked"""
        pass

    @abstractmethod
    async def is_booked(self, slot_id: int) -> bool:
        """Check if a time slot is booked"""
        pass

    @abstractmethod
    async def create(self, time_slot: TimeSlot) -> Optional[TimeSlot]:
        """Create a new time slot."""
        pass

    @abstractmethod
    async def update(self, slot_id: int, **kwargs) -> bool:
        """Update an existing time slot."""
        pass

    @abstractmethod
    async def delete(self, slot_id: int) -> bool:
        """Delete a time slot."""
        pass
