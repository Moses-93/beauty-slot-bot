from abc import ABC, abstractmethod
from typing import List

from src.application.dto.service import ServiceDTO


class AbstractServiceRepository(ABC):
    @abstractmethod
    async def get_active_services(self) -> List[ServiceDTO]:
        """Get all services."""
        pass

    @abstractmethod
    async def create(self, service_data: ServiceDTO) -> ServiceDTO:
        """Create a new service."""
        pass

    @abstractmethod
    async def update(self, service_id: int, **kwargs) -> bool:
        """Update an existing service."""
        pass

    @abstractmethod
    async def delete(self, service_id: int) -> None:
        """Delete a service by its ID."""
        pass
