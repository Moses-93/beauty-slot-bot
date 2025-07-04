from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.service import Service


class AbstractServiceRepository(ABC):
    @abstractmethod
    async def get(
        self, master_id: int, limit: int, offset: int
    ) -> Optional[List[Service]]:
        """Get all active services."""
        pass

    @abstractmethod
    async def get_by_id(self, service_id: int) -> Optional[Service]:
        """Get a service by its ID."""
        pass

    @abstractmethod
    async def create(self, service: Service) -> Optional[Service]:
        """Create a new service."""
        pass

    @abstractmethod
    async def update(self, service_id: int, **kwargs) -> bool:
        """Update an existing service."""
        pass

    @abstractmethod
    async def delete(self, service_id: int) -> bool:
        """Delete a service by its ID."""
        pass
