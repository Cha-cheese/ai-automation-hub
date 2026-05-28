import asyncio
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.orchestrator import automation_graph
from app.core.config import get_settings

settings = get_settings()

app = FastAPI()

class Req(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
async def automate(req: Req):
    session_id = str(uuid.uuid4())

    initial_state = {
        "user_input": req.message,
        "intent": "",
        "email_data": {},
        "summary": "",
        "category": "",
        "slack_sent": False,
        "calendar_event": {},
        "search_results": [],
        "final_response": "",
        "error": "",
    }

    try:
        # HARD TIMEOUT FIX (LEVEL 4)
        result = await asyncio.wait_for(
            asyncio.to_thread(automation_graph.invoke, initial_state),
            timeout=5
        )

        return {
            "session_id": session_id,
            "result": result.get("final_response", ""),
            "intent": result.get("intent", "general")
        }

    except asyncio.TimeoutError:
        return {
            "session_id": session_id,
            "result": "System timeout (agent too slow)",
            "intent": "timeout"
        }