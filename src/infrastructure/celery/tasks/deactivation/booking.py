from asgiref.sync import async_to_sync

from src.infrastructure.celery.celery_app import celery_app


@celery_app.task(name="deactivate_booking")
def deactivate(booking_id: int) -> None:
    """Celery task to deactivate a booking."""
    async_to_sync(_deactivate)(booking_id)


async def _deactivate(booking_id: int) -> None:
    """Internal function to deactivate a booking by its ID."""
    from src.main_container import get_container

    container = get_container()
    booking_use_case = container.resolve("DeactivateBookingUseCase")
    await booking_use_case(booking_id)
