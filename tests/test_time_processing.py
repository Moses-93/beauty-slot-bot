import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
from utils.time_processing import (
    get_busy_slots,
    check_slot,
    find_nearest_available_time,
)


@pytest.mark.asyncio
async def test_get_busy_slots():

    user_id = 1

    service = AsyncMock()
    service.duration = timedelta(minutes=40)

    date = AsyncMock()
    date.date = datetime.now().date()
    date.id = 1
    # Імітація бази даних та інших функцій
    with patch(
        "cache.cache.user_cache.get_user_cache", AsyncMock(return_value=(service, date))
    ):
        # Виклик функції
        busy_slots = await get_busy_slots(user_id)

        # Перевірка
        assert isinstance(busy_slots, list)
        assert all("start" in slot and "end" in slot for slot in busy_slots)


@pytest.mark.asyncio
async def test_find_nearest_available_time():
    user_id = 1
    current_time = datetime(2024, 10, 1, 12, 0)
    service_durations = AsyncMock()
    service_durations.duration = timedelta(hours=1)
    busy_slots = [
        {"start": current_time, "end": current_time + service_durations.durations}
    ]
    with patch(
        "cache.cache.user_cache.get_user_cache",
        AsyncMock(return_value=(service_durations,)),
    ):
        nearest_time = await find_nearest_available_time(
            user_id, current_time, busy_slots
        )
        assert nearest_time == current_time + timedelta(hours=1)


@pytest.mark.asyncio
async def test_check_slot_available():
    user_id = 1
    current_time = datetime(2024, 10, 1, 12, 0)
    busy_slots = [{"start": current_time, "end": current_time + timedelta(hours=1)}]

    # Мокаємо залежності
    service = AsyncMock()
    service.duration = timedelta(hours=1)

    date = AsyncMock()
    date.date = current_time.date()
    date.id = 1

    # Мокаємо кеш
    with patch(
        "cache.cache.user_cache.get_user_cache", AsyncMock(return_value=(service,))
    ):
        # Мокаємо функцію get_busy_slots
        with patch(
            "utils.time_processing.get_busy_slots", AsyncMock(return_value=busy_slots)
        ):
            # Викликаємо функцію
            slot = await check_slot(user_id, current_time)

            # Перевірка
            assert slot == current_time + timedelta(hours=1)


@pytest.mark.asyncio
async def test_check_slot_not_busy():
    user_id = 1
    current_time = datetime(2024, 10, 1, 12, 0)
    busy_slots = []
    with patch("utils.time_processing.get_busy_slots", return_value=busy_slots):
        slot = await check_slot(user_id, current_time)
        assert slot == current_time
