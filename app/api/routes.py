import uuid
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.orchestrator import automation_graph
from app.core.queue import add_job

app = FastAPI()


class Req(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "LEVEL 5 AI Automation Hub"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
async def automate(req: Req):
    session_id = str(uuid.uuid4())

    state = {
        "user_input": req.message,
        "intent": None,
        "final_response": ""
    }

    async def run_graph():
        automation_graph.invoke(state)

    # 🔥 LEVEL 5: queue execution (non-blocking)
    add_job(run_graph)

    return {
        "session_id": session_id,
        "status": "queued",
        "message": "Processing in background"
    }