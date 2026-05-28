from fastapi import APIRouter
from app.core.celery_app import celery

router = APIRouter()


@router.get("/result/{task_id}")
def get_result(task_id: str):

    task = celery.AsyncResult(task_id)

    if task.ready():
        return {
            "status": "done",
            "data": task.get()
        }

    return {"status": "processing"}