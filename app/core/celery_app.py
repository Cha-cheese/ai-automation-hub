from celery import Celery

celery = Celery(
    "ai_hub",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)