from celery import Celery
from celery import shared_task
import datetime

app = Celery("Urmart")

@shared_task()
def test_task():
    print("This is a test task.")