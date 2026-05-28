from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
import asyncio
import uuid
from app.core.config import get_settings

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    message: str
    session_id: str | None = None

@app.get("/")
def root():
    return {"status": "AI Automation Hub running"}

@app.post("/automate")
async def automate(req: Request):

    session_id = req.session_id or str(uuid.uuid4())

    initial_state = {
        "user_input": req.message,
        "intent": "",
        "final_response": "",
        "error": "",
    }

    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(automation_graph.invoke, initial_state),
            timeout=settings.request_timeout_seconds
        )

        return {
            "session_id": session_id,
            "result": result.get("final_response", "OK"),
            "intent": result.get("intent", "general"),
        }

    except asyncio.TimeoutError:
        return {
            "session_id": session_id,
            "result": "System timeout (agent too slow)",
            "intent": "timeout"
        }