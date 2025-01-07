import datetime
import os

from celery import Celery
from django.conf import settings
from .celerybeat_schedule import CELERY_BEAT_SCHEDULE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 排程時區
app.conf.timezone = "Asia/Taipei"
app.conf.enable_utc = False

app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
