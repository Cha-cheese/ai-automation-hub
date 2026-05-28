from celery import Celery
import os

celery = Celery(
    "ai_hub",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/1")
)