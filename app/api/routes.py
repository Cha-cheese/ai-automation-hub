from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from app.workers.tasks import run_automation

app = FastAPI()


class Req(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "AI Automation Hub running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
def automate(req: Req):

    job_id = str(uuid.uuid4())

    task = run_automation.delay(req.message)

    return {
        "job_id": job_id,
        "task_id": task.id,
        "status": "queued"
    }