import os

from celery import Celery
from celery.beat import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "todo_homework": {
        "task": "users.tasks.todo_homework",
        "schedule": crontab(minute="*/5")
    }
}

app.conf.beat_schedule = {
    "clear-temp-every-night": {
        "task": "users.tasks.clear_temp_data",
        "schedule": crontab(hour=3, minute=0),
    },
}

app.conf.beat_schedule = {
    "send-daily-email": {
        "task": "users.tasks.send_daily_email",
        "schedule": crontab(hour=9, minute=0),  # каждый день в 09:00
    },
}
