# app/celery/__init__.py
from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery("worker", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)
celery_app.conf.update(task_default_queue='tsp_tasks')

# Это нужно, чтобы Celery знал, где искать задачи
celery_app.autodiscover_tasks(['app.celery'])