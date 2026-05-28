import uuid
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.orchestrator import automation_graph

app = FastAPI()

class Req(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "AI Automation Hub running", "level": 4}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
async def automate(req: Req):
    session_id = str(uuid.uuid4())

    state = {
        "user_input": req.message,
        "intent": None,
        "email_data": None,
        "summary": None,
        "category": None,
        "slack_sent": False,
        "calendar_event": None,
        "search_results": [],
        "final_response": "",
        "error": None,
    }

    try:
        # LEVEL 4 SAFE EXECUTION (no freeze)
        result = await asyncio.wait_for(
            asyncio.to_thread(automation_graph.invoke, state),
            timeout=8
        )

        return {
            "session_id": session_id,
            "result": result.get("final_response", ""),
            "intent": result.get("intent", "general")
        }

    except Exception as e:
        return {
            "session_id": session_id,
            "result": "System error",
            "error": str(e),
            "intent": "error"
        }