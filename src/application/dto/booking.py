from dataclasses import dataclass
from datetime import time as Time, datetime
from typing import Optional
from pydantic import BaseModel


class BookingDTO(BaseModel):
    user_id: int
    service_id: int
    date_id: int
    time: Time
    reminder_time: Optional[datetime] = None


@dataclass
class TimeCheckResultDTO:
    is_available: bool
    time_offers: Optional[list[Time]] = None


@dataclass
class CreateBookingResultDTO:
    is_success: bool
    error_message: Optional[str] = None
