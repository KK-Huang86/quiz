import datetime
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 排程時區
app.conf.timezone = "Asia/Taipei"
app.conf.enable_utc = False


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
