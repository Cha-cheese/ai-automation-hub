from fastapi import FastAPI, Header
from app.workers.tasks import run_ai
from app.core.auth import verify_token
import uuid
from pydantic import BaseModel
from app.core.auth import login as auth_login

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


class LoginReq(BaseModel):
    username: str
    password: str


@app.post("/login")
def login_api(req: LoginReq):

    token = auth_login(req.username, req.password)

    if not token:
        return {"error": "invalid credentials"}

    return {
        "token": token
    }