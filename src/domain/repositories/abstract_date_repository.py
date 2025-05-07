from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.date import Date


class AbstractDateRepository(ABC):
    @abstractmethod
    def get_dates(self) -> List[Date]:
        """Get all dates."""
        pass

    @abstractmethod
    def get_date_by_id(self, date_id: int) -> Date:
        """Get a date by its ID."""
        pass

    @abstractmethod
    def create(self, date_data: Date) -> Date:
        """Create a new date."""
        pass

    @abstractmethod
    def update(self, date_id: int, date: Date) -> Date:
        """Update an existing date."""
        pass

    @abstractmethod
    def delete(self, date_id: int) -> None:
        """Delete a date by its ID."""
        pass
