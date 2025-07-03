from dataclasses import dataclass
from datetime import date as Date, time as Time
from .base_event import Event


@dataclass(kw_only=True)
class BookingCreated(Event):
    master_chat_id: int
    client_chat_id: int
    service: str
    date: Date
    time: Time
