from asgiref.sync import async_to_sync

from src.main_container import get_container
from src.application.use_cases.date import DeactivateDateUseCase
from src.infrastructure.celery.celery_app import celery_app


@celery_app.task(name="deactivate_date")
def deactivate(date_id: int) -> None:
    """
    Celery task to deactivate a date by its ID.
    """
    async_to_sync(_deactivate)(date_id)


async def _deactivate(date_id: int) -> None:
    """
    Internal function to deactivate a date by its ID.
    """
    container = get_container()
    use_case = container.resolve(DeactivateDateUseCase)
    await use_case(date_id)
