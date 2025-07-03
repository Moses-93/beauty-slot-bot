from dataclasses import dataclass
from datetime import time, date as Date
from typing import List
from pydantic import BaseModel, Field


class TimeSlotDTO(BaseModel):
    master_id: int
    date: Date
    start: time
    end: time
    is_active: bool = Field(default=True)
    is_booked: bool = Field(default=False)


@dataclass
class TimeCheckResultDTO:
    """
    Data Transfer Object for the result of a time check.

    Attributes:
        is_available (bool): Indicates if the requested time is available.
        time_offers (List[time]): Optional list of alternative time slots if the requested time is not available.
    """

    is_available: bool
    time_offers: List[time] = None
