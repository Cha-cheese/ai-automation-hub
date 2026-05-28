import uuid
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.orchestrator import automation_graph

app = FastAPI()

class Req(BaseModel):
    message: str


# simple in-memory job store (LEVEL 5 lightweight queue)
JOB_RESULTS = {}


@app.get("/")
def root():
    return {"status": "FINAL LEVEL 5 AI Automation Hub"}


@app.get("/health")
def health():
    return {"status": "ok"}


async def run_agent(session_id: str, message: str):
    state = {
        "user_input": message,
        "intent": None,
        "final_response": ""
    }

    try:
        result = await asyncio.to_thread(automation_graph.invoke, state)
        JOB_RESULTS[session_id] = {
            "status": "done",
            "result": result.get("final_response"),
            "intent": result.get("intent")
        }

    except Exception as e:
        JOB_RESULTS[session_id] = {
            "status": "error",
            "error": str(e)
        }


@app.post("/automate")
async def automate(req: Req):
    session_id = str(uuid.uuid4())

    JOB_RESULTS[session_id] = {"status": "processing"}

    # 🔥 NON-BLOCKING
    asyncio.create_task(run_agent(session_id, req.message))

    return {
        "session_id": session_id,
        "status": "queued"
    }


@app.get("/result/{session_id}")
def get_result(session_id: str):
    return JOB_RESULTS.get(session_id, {"status": "not_found"})