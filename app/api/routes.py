from fastapi import FastAPI, Header
from app.workers.tasks import run_ai
from app.core.auth import verify_token
import uuid
from pydantic import BaseModel

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

class LoginReq(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(req: LoginReq):

    if req.username == "admin" and req.password == "admin123":
        return {
            "token": "dev-token-123"
        }

    return {"error": "invalid credentials"}