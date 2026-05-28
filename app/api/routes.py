from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
from app.core.config import get_settings
import asyncio
import uuid
from datetime import datetime

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(automation_graph.invoke, {
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
            }),
            timeout=settings.request_timeout_seconds
        )

        return {
            "session_id": session_id,
            "result": result.get("final_response"),
            "intent": result.get("intent"),
        }

    except asyncio.TimeoutError:
        return {
            "session_id": session_id,
            "result": "System timeout (agent too slow)",
            "intent": "timeout"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))