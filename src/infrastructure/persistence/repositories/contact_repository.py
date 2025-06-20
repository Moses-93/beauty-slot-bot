from typing import Union
from sqlalchemy import delete, select, update
from src.domain.repositories.abstract_contact_repository import (
    AbstractContactRepository,
)
from src.application.dto.contact import ContactDTO
from src.infrastructure.persistence.repositories.base_repository import BaseRepository
from src.infrastructure.persistence.models import ContactModel


class ContactRepository(AbstractContactRepository):
    def __init__(self, factory_session):
        self._base_repo = BaseRepository(factory_session, ContactModel)

    async def get(self) -> Union[ContactDTO, None]:
        query = select(ContactModel)
        result = await self._base_repo.read(query, single=True)
        if not result:
            return None
        return ContactDTO(
            id=result.id,
            user_id=result.user_id,
            phone_number=result.phone_number,
            address=result.address,
            telegram_link=result.telegram_link,
            instagram_link=result.instagram_link,
            google_maps_link=result.google_maps_link,
            about=result.about,
            work_start_time=result.work_start_time,
            work_end_time=result.work_end_time,
        )

    async def create(self, contact: ContactDTO) -> Union[ContactDTO, None]:
        result = await self._base_repo.create(
            user_id=contact.user_id,
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
