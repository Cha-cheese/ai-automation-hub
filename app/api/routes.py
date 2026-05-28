import asyncio
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.orchestrator import automation_graph
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title="AI Automation Hub")

# -------------------------
# HEALTH CHECK (FIX 404)
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "AI Automation Hub running"}

# -------------------------
# REQUEST MODEL
# -------------------------
class Req(BaseModel):
    message: str

# -------------------------
# MAIN ORCHESTRATION
# -------------------------
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
        # 🔥 HARD GUARD (prevent Render freeze)
        result = await asyncio.wait_for(
            asyncio.to_thread(automation_graph.invoke, initial_state),
            timeout=15,   # LEVEL 4 SAFE LIMIT
        )

        return {
            "session_id": session_id,
            "result": result.get("final_response", "No response"),
            "intent": result.get("intent", "unknown"),
        }

    except asyncio.TimeoutError:
        return {
            "session_id": session_id,
            "result": "System timeout (agent too slow)",
            "intent": "timeout"
        }

    except Exception as e:
        return {
            "session_id": session_id,
            "result": f"System error: {str(e)}",
            "intent": "error"
        }