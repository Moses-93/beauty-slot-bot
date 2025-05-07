from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Contact:
    """Class representing a contact entity."""

    id: Optional[int] = field(default=None)
    user_id: Optional[int] = field(default=None)
    phone_number: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)
    telegram_link: Optional[str] = field(default=None)
    instagram_link: Optional[str] = field(default=None)
    google_maps_link: Optional[str] = field(default=None)
    about: Optional[str] = field(default=None)
