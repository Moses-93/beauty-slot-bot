from typing import Optional
from sqlalchemy import select, update, delete

from src.domain.repositories.abstract_date_repository import AbstractDateRepository
from src.application.dto.date import DateDTO
from src.infrastructure.persistence.models import DateModel
from .base_repository import BaseRepository


class DateRepository(AbstractDateRepository):
    def __init__(self, factory_session):
        self._base_repo = BaseRepository(factory_session, DateModel)

    async def get_active_dates(self) -> list[DateDTO]:
        """Get all dates."""
        result = await self._base_repo.read(select(DateModel).filter_by(is_active=True))
        return [
            DateDTO(
                date=date.date,
                deactivation_time=date.deactivation_time,
                is_active=date.is_active,
            )
            for date in result
        ]

    async def get_date_by_id(self, date_id: int) -> Optional[DateDTO]:
        """Get a date by its ID."""
        result = await self._base_repo.read_by_id(date_id)
        if result:
            return DateDTO(
                id=result.id,
                date=result.date,
                deactivation_time=result.deactivation_time,
                is_active=result.is_active,
            )
        return None

    async def create(self, date: DateDTO) -> Optional[DateDTO]:
        """Create a new date."""
        created_date = await self._base_repo.create(date.model_dump())
        if created_date:
            return DateDTO(
                id=created_date.id,
                date=created_date.date,
                deactivation_time=created_date.deactivation_time,
                is_active=created_date.is_active,
            )
        return None

    async def update(self, date_id: int, **kwargs) -> bool:
        """Update an existing date."""
        query = update(DateModel).where(DateModel.id == date_id).values(**kwargs)
        result = await self._base_repo.update(query)
        return result

    async def delete(self, date_id: int) -> bool:
        """Delete a date."""
        query = delete(DateModel).where(DateModel.id == date_id)
        result = await self._base_repo.delete(query)
        return result
