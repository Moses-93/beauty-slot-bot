from src.core.config import get_settings


class Config:

    _settings = get_settings()

    broker_url = _settings.redis_url("broker")

    timezone = "Europe/Kyiv"

    broker_connection_retry_on_startup = True

    task_serializer = "json"
    accept_content = ["json"]

    task_routes = {
        "infrastructure.celery.tasks.deactivation.*": {"queue": "deactivation"},
        "infrastructure.celery.tasks.reminders.*": {"queue": "reminders"},
    }
    task_default_queue = "default"
