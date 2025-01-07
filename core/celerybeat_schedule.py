from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "test_task1": {
        "task": "urmart.task.test_task",
        "schedule": crontab(minute=20, hour=14),
    },
    "generate_shop_sales_stats_daily": {
        "task": "urmart.task.generate_shop_sales_stats",
        "schedule": crontab(minute=20, hour=14),
    },
}
