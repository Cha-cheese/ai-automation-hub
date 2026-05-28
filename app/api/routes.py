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


@app.get("/")
def root():
    return {"status": "AI Automation Hub running"}


@app.post("/automate")
async def automate(req: Req):

    session_id = str(uuid.uuid4())

    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(
                automation_graph.invoke,
                {"user_input": req.message, "intent": ""}
            ),
            timeout=10  # 🔥 FIX: ลดจาก 45s → 10s
        )

        return {
            "session_id": session_id,
            "result": result["final_response"],
            "intent": result["intent"]
        }

    except asyncio.TimeoutError:
        return {
            "session_id": session_id,
            "result": "timeout (agent optimized mode failed)",
            "intent": "timeout"
        }