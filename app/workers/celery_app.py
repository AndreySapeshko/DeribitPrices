from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "deribit_prices",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

import app.workers.tasks

celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.workers.tasks.fetch_prices",
        "schedule": 60.0,
    }
}


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
