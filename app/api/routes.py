from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from app.agents.orchestrator import automation_graph

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

    session_id = str(uuid.uuid4())

    result = automation_graph({
        "user_input": req.message
    })

    return {
        "session_id": session_id,
        "result": result.get("final_response"),
        "intent": result.get("intent")
    }