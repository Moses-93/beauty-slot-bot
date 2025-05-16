from abc import ABC, abstractmethod
from typing import List

from src.application.dto.date import DateDTO


class AbstractDateRepository(ABC):
    @abstractmethod
    async def get_dates(self) -> List[DateDTO]:
        """Get all dates."""
        pass

    @abstractmethod
    async def get_date_by_id(self, date_id: int) -> DateDTO:
        """Get a date by its ID."""
        pass

    @abstractmethod
    async def create(self, date_data: DateDTO) -> DateDTO:
        """Create a new date."""
        pass

    @abstractmethod
    async def update(self, date_id: int, date: DateDTO) -> DateDTO:
        """Update an existing date."""
        pass

    @abstractmethod
    async def delete(self, date_id: int) -> None:
        """Delete a date by its ID."""
        pass
