celery -A infrastructure.celery.celery_app worker --loglevel=info --queues reminders,deactivation,default
