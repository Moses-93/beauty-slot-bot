import logging
from celery import Celery

from .celeryconfig import Config

logger = logging.getLogger(__name__)

celery_app = Celery("beauty_slot")
celery_app.config_from_object(Config)

logger.info("Autodiscovering Celery tasks...")

celery_app.autodiscover_tasks(
    [
        "infrastructure.celery.tasks.deactivation",
        "infrastructure.celery.tasks.reminders",
    ]
)
