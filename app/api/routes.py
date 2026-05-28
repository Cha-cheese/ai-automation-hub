from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
import uuid
import asyncio
from datetime import datetime

app = FastAPI()

class Req(BaseModel):
    message: str
    session_id: str = None


@app.get("/")
def home():
    return {"status": "AI Automation Hub running"}


@app.post("/automate")
async def automate(req: Req):
    session = req.session_id or str(uuid.uuid4())

    state = {
        "user_input": req.message,
        "intent": "general",
        "email_data": {},
        "summary": "",
        "category": "",
        "slack_sent": False,
        "calendar_event": {},
        "search_results": [],
        "final_response": "",
        "error": ""
    }

    try:
        # 🔥 HARD FIX TIMEOUT
        result = await asyncio.to_thread(automation_graph.invoke, state)

        return {
            "session_id": session,
            "result": result.get("final_response", "done"),
            "intent": result.get("intent", "general")
        }

    except Exception as e:
        return {
            "session_id": session,
            "result": f"error: {str(e)}",
            "intent": "error"
        }