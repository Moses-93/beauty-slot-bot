from dataclasses import dataclass
from datetime import time
from typing import List


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
