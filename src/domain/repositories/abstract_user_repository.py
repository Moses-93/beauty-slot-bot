from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> Optional[User]:
        """
        Create a new user.
        """
        pass

    @abstractmethod
    async def get_user_by_chat_id(self, chat_id: str) -> Optional[User]:
        """
        Get a user by their chat ID.
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID"""
        pass

    @abstractmethod
    async def is_exist(self, chat_id: str) -> bool:
        """
        Check if a user exists by their chat ID.
        """
        pass
