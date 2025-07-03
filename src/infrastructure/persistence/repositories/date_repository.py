from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.abstract_time_slot_repository import (
    AbstractTimeSlotRepository,
)
from src.domain.entities.time import TimeSlot
from src.infrastructure.persistence.models import TimeSlotModel
from .base_repository import BaseRepository


class TimeSlotRepository(AbstractTimeSlotRepository):
    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        self._base_repo = BaseRepository(factory_session, TimeSlotModel)

    async def get_active_slots(
        self, master_id: int, limit: int, offset: int
    ) -> Optional[List[TimeSlot]]:
        """Get active time slots for a master."""
        query = (
            select(TimeSlotModel)
            .filter_by(
                master_id=master_id,
                is_active=True,
                is_booked=False,
            )
            .limit(limit)
            .offset(offset)
        )
        slots = await self._base_repo.read(query)
        if not slots:
            return None

        return [self._to_entity(slot) for slot in slots]

    async def get_slot_by_id(self, slot_id: int) -> Optional[TimeSlot]:
        """Get a time slot by its ID."""
        slot = await self._base_repo.read_by_id(slot_id)
        return self._to_entity(slot) if slot else None

    async def mark_as_booked(self, slot_id: int) -> bool:
        """Mark a time slot as booked"""
        query = (
            update(TimeSlotModel)
            .where(TimeSlotModel.id == slot_id, TimeSlotModel.is_booked == False)
            .values(is_booked=True)
        )
        result = await self._base_repo.update(query)
        return result

    async def create(self, time_slot: TimeSlot) -> Optional[TimeSlot]:
        """Create a new time slot."""
        created_slot = await self._base_repo.create(self._to_model(time_slot))
        if created_slot:
            time_slot.id = created_slot.id
            return time_slot

        return None

    async def update(self, slot_id: int, **kwargs) -> bool:
        """Update an existing time slot."""
        query = (
            update(TimeSlotModel).where(TimeSlotModel.id == slot_id).values(**kwargs)
        )
        result = await self._base_repo.update(query)
        return result

    async def delete(self, slot_id: int) -> bool:
        """Delete a time slot."""
        query = delete(TimeSlotModel).where(TimeSlotModel.id == slot_id)
        result = await self._base_repo.delete(query)
        return result

    def _to_entity(self, model: TimeSlotModel) -> TimeSlot:
        """Convert a TimeSlotModel to a TimeSlot entity."""
        return TimeSlot(
            id=model.id,
            master_id=model.master_id,
            date=model.date,
            start=model.start_time,
            end=model.end_time,
            is_active=model.is_active,
            is_booked=model.is_booked,
        )

    def _to_model(self, entity: TimeSlot) -> TimeSlotModel:
        """Convert a TimeSlot entity to a TimeSlotModel."""
        return TimeSlotModel(
            master_id=entity.master_id,
            date=entity.date,
            start_time=entity.start,
            end_time=entity.end,
            is_active=entity.is_active,
            is_booked=entity.is_booked,
        )
