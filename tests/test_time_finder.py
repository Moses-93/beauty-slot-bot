import pytest
from datetime import time, timedelta

from src.application.services.time_finder import AvailableTimeFinder
from src.domain.entities.time import TimeSlot


class FakeContact:
    work_start_time = time(9, 0)
    work_end_time = time(12, 0)


class FakeContactRepo:
    async def get(self):
        return FakeContact()


@pytest.mark.asyncio
async def test_finder_finds_free_slots():
    finder = AvailableTimeFinder(FakeContactRepo())
    busy_slots = [
        TimeSlot(time(10, 0), time(10, 30)),
        TimeSlot(time(11, 0), time(11, 30)),
    ]
    result = await finder.find_nearby(
        desired_time=time(10, 0),
        busy_slots=busy_slots,
        service_duration=timedelta(minutes=30),
    )
    assert time(9, 30) in result
    assert time(10, 30) in result


@pytest.mark.asyncio
async def test_finder_returns_none_when_all_busy():
    finder = AvailableTimeFinder(FakeContactRepo())
    busy_slots = [
        TimeSlot(time(9, 0), time(9, 30)),
        TimeSlot(time(9, 30), time(10, 0)),
        TimeSlot(time(10, 0), time(10, 30)),
        TimeSlot(time(10, 30), time(11, 0)),
        TimeSlot(time(11, 0), time(11, 30)),
        TimeSlot(time(11, 30), time(12, 0)),
    ]
    result = await finder.find_nearby(
        desired_time=time(9, 0),
        busy_slots=busy_slots,
        service_duration=timedelta(minutes=30),
    )
    assert result == []


@pytest.mark.asyncio
async def test_finder_handles_partial_overlap():
    finder = AvailableTimeFinder(FakeContactRepo())
    busy_slots = [
        TimeSlot(time(9, 15), time(9, 45)),
    ]
    result = await finder.find_nearby(
        desired_time=time(9, 0),
        busy_slots=busy_slots,
        service_duration=timedelta(minutes=30),
    )
    assert time(10, 0) in result


@pytest.mark.asyncio
async def test_finder_respects_service_duration():
    finder = AvailableTimeFinder(FakeContactRepo())
    result = await finder.find_nearby(
        desired_time=time(9, 0),
        busy_slots=[],
        service_duration=timedelta(minutes=60),
    )

    assert time(10, 0) in result


@pytest.mark.asyncio
async def test_finder_allows_exact_border_slot():
    finder = AvailableTimeFinder(FakeContactRepo())
    busy_slots = [TimeSlot(time(9, 0), time(9, 30))]
    result = await finder.find_nearby(
        desired_time=time(9, 0),
        busy_slots=busy_slots,
        service_duration=timedelta(minutes=30),
    )
    assert time(9, 30) in result


@pytest.mark.asyncio
async def test_finder_respects_custom_desired_time():
    finder = AvailableTimeFinder(FakeContactRepo())
    result = await finder.find_nearby(
        desired_time=time(10, 0),
        busy_slots=[],
        service_duration=timedelta(minutes=30),
    )
    assert time(9, 0) not in result


@pytest.mark.asyncio
async def test_finder_returns_empty_if_service_duration_too_large():
    finder = AvailableTimeFinder(FakeContactRepo())
    result = await finder.find_nearby(
        desired_time=time(9, 0),
        busy_slots=[],
        service_duration=timedelta(hours=5),  # 9:00–14:00
    )
    assert result == []


@pytest.mark.asyncio
async def test_finder_returns_unique_slots():
    finder = AvailableTimeFinder(FakeContactRepo())
    result = await finder.find_nearby(
        desired_time=time(9, 0),
        busy_slots=[],
        service_duration=timedelta(minutes=30),
    )
    assert len(result) == len(set(result))  # Uniqueness


@pytest.mark.asyncio
async def test_finder_handles_desired_time_before_work():
    finder = AvailableTimeFinder(FakeContactRepo())
    result = await finder.find_nearby(
        desired_time=time(8, 0),
        busy_slots=[],
        service_duration=timedelta(minutes=30),
    )
    assert result == []


@pytest.mark.asyncio
async def test_finder_handles_desired_time_after_work():
    finder = AvailableTimeFinder(FakeContactRepo())
    result = await finder.find_nearby(
        desired_time=time(13, 0),
        busy_slots=[],
        service_duration=timedelta(minutes=30),
    )
    assert result == []
