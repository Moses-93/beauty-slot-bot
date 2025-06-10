from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_user_by_chat_id(self, chat_id: str) -> Optional[User]:
        """
        Get a user by their chat ID.
        """
        pass

    @abstractmethod
    async def is_exist(self, chat_id: str) -> bool:
        """
        Check if a user exists by their chat ID.
        """
        pass
