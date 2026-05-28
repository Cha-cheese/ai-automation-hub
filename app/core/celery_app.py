from celery import Celery

celery = Celery(
    "ai_hub",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1",
)

celery.conf.task_track_started = True