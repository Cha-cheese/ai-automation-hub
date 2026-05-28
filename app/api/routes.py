from fastapi import FastAPI, Header
from app.workers.tasks import run_ai
from app.core.auth import verify_token
import uuid

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
def automate(req: dict, authorization: str = Header(None)):

    user = verify_token(authorization)

    if not user:
        return {"error": "unauthorized"}

    task = run_ai.delay(req["message"], user["user_id"])

    return {
        "task_id": task.id,
        "status": "processing"
    }