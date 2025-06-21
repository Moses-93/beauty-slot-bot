from datetime import time, timedelta
from src.domain.repositories.abstract_booking_repository import (
    AbstractBookingRepository,
)
from src.domain.entities.time import TimeSlot
from src.application.dto.time import TimeCheckResultDTO
from src.application.services.time_finder import AvailableTimeFinder


class CheckBookingAvailabilityUseCase:
    def __init__(
        self, booking_repo: AbstractBookingRepository, time_finder: AvailableTimeFinder
    ):
        self._booking_repo = booking_repo
        self._time_finder = time_finder

    async def check_time(
        self, date_id: int, requested_time: time, service_duration: timedelta
    ) -> TimeCheckResultDTO:
        busy_slots = await self._booking_repo.get_busy_slots(date_id)
        user_time_slot = TimeSlot.create_with_duration(requested_time, service_duration)
        is_available = not any(
            busy_slot.overlaps(user_time_slot) for busy_slot in busy_slots
        )
        if is_available:
            return TimeCheckResultDTO(is_available=True)
        else:
            nearby_slots = await self._time_finder.find_nearby(
                requested_time, busy_slots, service_duration
            )
            return TimeCheckResultDTO(is_available=False, time_offers=nearby_slots)
