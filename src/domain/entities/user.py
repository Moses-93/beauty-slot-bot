from dataclasses import dataclass
from typing import Optional, List

from src.domain.enums.user_role import UserRole
from src.domain.entities.booking import Booking


@dataclass
class User:
    name: str
    username: Optional[str] = None
    chat_id: str
    role: UserRole
    bookings: Optional[List[Booking]] = None

    def is_master(self) -> bool:
        """
        Check if the user is an admin.
        """
        return self.role == UserRole.MASTER

    def is_client(self) -> bool:
        """
        Check if the user is a client.
        """
        return self.role == UserRole.CLIENT
