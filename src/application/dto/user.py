from dataclasses import dataclass, field
from typing import Optional

from src.domain.enums.user_role import UserRole


@dataclass
class UserDTO:
    name: str
    username: Optional[str] = None
    chat_id: str
    role: UserRole = field(default=UserRole.CLIENT)
