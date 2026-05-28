from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import asyncio

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
async def automate(req: Req):
    session_id = str(uuid.uuid4())

    state = {
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
            "result": f"error: {str(e)}",
            "intent": "error"
        }