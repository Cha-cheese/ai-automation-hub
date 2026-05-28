from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from app.agents.orchestrator import automation_graph
from app.core.memory import Memory

app = FastAPI()
memory = Memory()


class Req(BaseModel):
    message: str
    session_id: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
def automate(req: Req):

    session_id = req.session_id or str(uuid.uuid4())

    prev_memory = memory.load(session_id)

    state = {
        "user_input": req.message,
        "memory": prev_memory
    }

    result = automation_graph(state)

    memory.save(session_id, result)

    return {
        "session_id": session_id,
        "result": result.get("final_response"),
        "intent": result.get("intent")
    }

@app.get("/")
def root():
    return {
        "status": "AI Automation Hub running",
        "docs": "/docs",
        "health": "/health",
        "endpoint": "/automate"
    }