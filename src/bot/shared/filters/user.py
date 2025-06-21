from typing import Optional, Set, Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole


class RoleFilter(BaseFilter):
    def __init__(self, roles: Set[UserRole]):
        self.roles = roles

    async def __call__(
        self, event: Union[Message, CallbackQuery], *, user: Optional[User] = None
    ) -> bool:
        """
        Check if the user has one of the specified roles.
        """
        return bool(user) and user.role in self.roles
