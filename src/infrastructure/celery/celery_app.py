from celery import Celery

from .celeryconfig import Config

celery_app = Celery("tasks")
celery_app.config_from_object(Config)
