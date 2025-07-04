from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.abstract_service_repository import (
    AbstractServiceRepository,
)
from src.domain.entities.service import Service
from src.infrastructure.persistence.models import ServiceModel
from .base_repository import BaseRepository


class ServiceRepository(AbstractServiceRepository):
    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        self._base_repo = BaseRepository(factory_session, ServiceModel)

    async def get(
        self, master_id: int, limit: int, offset: int
    ) -> Optional[List[Service]]:
        """Get active services."""
        result = await self._base_repo.read(
            select(ServiceModel)
            .filter_by(is_active=True, master_id=master_id)
            .limit(limit)
            .offset(offset)
        )
        if result is None:
            return None
        return [self._to_entity(service) for service in result]

    async def get_by_id(self, service_id: int) -> Optional[Service]:
        """Get a service by its ID"""
        service = await self._base_repo.read_by_id(service_id)
        if service is None:
            return None
        return self._to_entity(service)

    async def create(self, service: Service) -> Service:
        """Create a new service."""
        created_service = await self._base_repo.create(service.model_dump())
        return Service(
            id=created_service.id,
            title=created_service.title,
            price=created_service.price,
            duration=created_service.duration,
        )

    async def update(self, service_id: int, **kwargs) -> bool:
        """Update an existing service."""
        query = (
            update(ServiceModel).where(ServiceModel.id == service_id).values(**kwargs)
        )
        result = await self._base_repo.update(query)
        return result

    async def delete(self, service_id: int) -> bool:
        """Delete a service."""
        query = delete(ServiceModel).where(ServiceModel.id == service_id)
        result = await self._base_repo.delete(query)
        return result

    def _to_entity(self, model: ServiceModel) -> Service:
        """Convert a ServiceModel to a Service entity."""
        return Service(
            id=model.id,
            master_id=model.master_id,
            title=model.title,
            price=model.price,
            duration=model.duration,
        )
