from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.service import Service


class AbstractServiceRepository(ABC):
    @abstractmethod
    def get_services(self) -> List[Service]:
        """Get all services."""
        pass

    @abstractmethod
    def get_service_by_id(self, service_id: int) -> Service:
        """Get a service by its ID."""
        pass

    @abstractmethod
    def create(self, service_data: Service) -> Service:
        """Create a new service."""
        pass

    @abstractmethod
    def update(self, service_id: int, service: Service) -> Service:
        """Update an existing service."""
        pass

    @abstractmethod
    def delete(self, service_id: int) -> None:
        """Delete a service by its ID."""
        pass
