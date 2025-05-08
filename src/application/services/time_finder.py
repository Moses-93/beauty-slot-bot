from datetime import datetime, time, timedelta
from typing import List, Optional

from src.domain.entities.time import TimeSlot
from src.domain.repositories.abstract_contact_repository import (
    AbstractContactRepository,
)


class AvailableTimeFinder:
    def __init__(self, contact_repo: AbstractContactRepository):
        self._contact_repo = contact_repo

    async def find_nearby(
        self,
        desired_time: time,
        busy_slots: List[TimeSlot],
        service_duration: timedelta,
    ) -> List[time]:
        """
        Find available time slots around the desired time.
        """
        start_time, end_time = await self._get_work_schedule()

        available_slots = []

        previous_slot = self._find_previous_slot(
            start_time, end_time, desired_time, busy_slots, service_duration
        )
        if previous_slot:
            available_slots.append(previous_slot)
        next_slot = self._find_next_slot(
            start_time, end_time, desired_time, busy_slots, service_duration
        )
        if next_slot:
            available_slots.append(next_slot)

        return available_slots

    async def _get_work_schedule(self):
        """
        Prepare data for the time slot finder.
        """
        contact = await self._contact_repo.get()
        start_time = datetime.combine(datetime.today(), contact.work_start_time)
        end_time = datetime.combine(datetime.today(), contact.work_end_time)
        return start_time, end_time

    def _find_previous_slot(
        self,
        start_time: datetime,
        end_time: datetime,
        desired_time: time,
        busy_slots: List[TimeSlot],
        service_duration: timedelta,
    ) -> Optional[time]:
        """
        Find the previous available time slot before the desired time.
        """

        current_dt = datetime.combine(datetime.today(), desired_time) - service_duration

        while start_time <= current_dt <= end_time - service_duration:
            candidate = TimeSlot.create_with_duration(
                current_dt.time(), service_duration
            )
            if not any(slot.overlaps(candidate) for slot in busy_slots):
                return candidate.start
            current_dt -= service_duration
        return None

    def _find_next_slot(
        self,
        start_time: datetime,
        end_time: datetime,
        desired_time: time,
        busy_slots: List[TimeSlot],
        service_duration: timedelta,
    ) -> Optional[time]:
        """
        Find the next available time slot after the desired time.
        """

        current_dt = datetime.combine(datetime.today(), desired_time) + service_duration

        while start_time <= current_dt <= end_time - service_duration:
            candidate = TimeSlot.create_with_duration(
                current_dt.time(), service_duration
            )
            if not any(slot.overlaps(candidate) for slot in busy_slots):
                return candidate.start
            current_dt += service_duration
        return None
