from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


from src.domain.repositories.abstract_user_repository import AbstractUserRepository
from src.domain.entities.user import User
from src.infrastructure.persistence.models import UserModel
from .base_repository import BaseRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        self._base_repo = BaseRepository(factory_session, UserModel)

    async def get_user_by_chat_id(self, chat_id: str) -> Optional[User]:
        """Get a user by their chat ID."""
        query = select(UserModel).filter(UserModel.chat_id == chat_id)
        result = await self._base_repo.read(query, single=True)
        if result:
            return User(
                id=result.id,
                name=result.name,
                username=result.username,
                chat_id=result.chat_id,
                role=result.role,
            )
        return None

    async def is_exist(self, chat_id: str) -> bool:
        """Check if a user exists by their chat ID."""
        query = select(UserModel).filter(UserModel.chat_id == chat_id)
        result = await self._base_repo.read(query, single=True)
        return result is not None
