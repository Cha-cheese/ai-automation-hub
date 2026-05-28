from fastapi import FastAPI, Header
from pydantic import BaseModel
import uuid

from app.agents.orchestrator import automation_graph
from app.core.auth import verify
from app.core.db import db

app = FastAPI()


class Req(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "AI Automation Hub running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
def automate(req: Req, authorization: str = Header(None)):

    user = verify(authorization)

    if not user:
        return {"error": "unauthorized"}

    session_id = str(uuid.uuid4())

    memory = db.get(user, "memory")

    result = automation_graph({
        "user_input": req.message,
        "memory": memory
    })

    db.save(user, "memory", result)

    return {
        "session_id": session_id,
        "result": result.get("final_response"),
        "intent": result.get("intent")
    }


from app.core.auth import login


@app.post("/login")
def login_api(data: dict):
    token = login(data["username"], data["password"])

    if not token:
        return {"error": "invalid credentials"}

    return {"token": token}