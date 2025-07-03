from dataclasses import dataclass, field
from typing import Optional
from datetime import time


@dataclass
class ContactDTO:
    id: Optional[int] = field(default=None)
    master_id: Optional[int] = field(default=None)
    phone_number: Optional[str] = field(default=None)
    address: str = field(default=None)
    telegram_link: Optional[str] = field(default=None)
    instagram_link: Optional[str] = field(default=None)
    google_maps_link: Optional[str] = field(default=None)
    about: Optional[str] = field(default=None)
    work_start_time: time = field(default=None)
    work_end_time: time = field(default=None)
