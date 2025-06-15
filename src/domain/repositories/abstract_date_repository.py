from abc import ABC, abstractmethod
from typing import List, Optional

from src.application.dto.date import DateDTO


class AbstractDateRepository(ABC):
    @abstractmethod
    async def get_active_dates(self, limit: int, offset: int) -> List[DateDTO]:
        """Get all dates."""
        pass

    @abstractmethod
    async def get_date_by_id(self, date_id: int) -> Optional[DateDTO]:
        """Get a date by its ID."""
        pass

    @abstractmethod
    async def create(self, date_data: DateDTO) -> Optional[DateDTO]:
        """Create a new date."""
        pass

    @abstractmethod
    async def update(self, date_id: int, **kwargs) -> bool:
        """Update an existing date."""
        pass

    @abstractmethod
    async def delete(self, date_id: int) -> bool:
        """Delete a date by its ID."""
        pass
