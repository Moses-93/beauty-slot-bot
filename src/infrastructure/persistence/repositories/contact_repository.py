from typing import Optional
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.repositories.abstract_contact_repository import (
    AbstractContactRepository,
)
from src.application.dto.contact import ContactDTO
from src.infrastructure.persistence.repositories.base_repository import BaseRepository
from src.infrastructure.persistence.models import ContactModel


class ContactRepository(AbstractContactRepository):
    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        self._base_repo = BaseRepository(factory_session, ContactModel)

    async def get(self, master_id: int) -> Optional[ContactDTO]:
        query = select(ContactModel).filter_by(master_id=master_id)
        result = await self._base_repo.read(query, single=True)
        if not result:
            return None
        return ContactDTO(
            id=result.id,
            master_id=result.master_id,
            phone_number=result.phone_number,
            address=result.address,
            telegram_link=result.telegram_link,
            instagram_link=result.instagram_link,
            google_maps_link=result.google_maps_link,
            about=result.about,
            work_start_time=result.work_start_time,
            work_end_time=result.work_end_time,
        )

    async def create(self, contact: ContactDTO) -> Optional[ContactDTO]:
        result = await self._base_repo.create(
            master_id=contact.master_id,
            phone_number=contact.phone_number,
            address=contact.address,
            telegram_link=contact.telegram_link,
            instagram_link=contact.instagram_link,
            google_maps_link=contact.google_maps_link,
            about=contact.about,
            work_start_time=contact.work_start_time,
            work_end_time=contact.work_end_time,
        )
        return result

    async def update(self, id: int, **kwargs) -> bool:
        query = update(ContactModel).where(ContactModel.id == id).values(**kwargs)
        result = await self._base_repo.update(query)
        return result

    async def delete(self, id: int) -> bool:
        query = delete(ContactModel).where(ContactModel.id == id)
        result = await self._base_repo.delete(query)
        return result
