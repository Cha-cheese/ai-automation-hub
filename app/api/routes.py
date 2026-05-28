from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
from upstash_redis import Redis
from app.core.config import get_settings
import asyncio, uuid, json
from datetime import datetime

settings = get_settings()

app = FastAPI(title="AI Automation Hub", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis optional
redis = None
if settings.upstash_redis_rest_url and settings.upstash_redis_rest_token:
    redis = Redis(
        url=settings.upstash_redis_rest_url,
        token=settings.upstash_redis_rest_token
    )

class AutomationRequest(BaseModel):
    message: str
    session_id: str = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
async def automate(req: AutomationRequest):
    session_id = req.session_id or str(uuid.uuid4())

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
        result = await asyncio.wait_for(
            asyncio.to_thread(automation_graph.invoke, initial_state),
            timeout=25,   # 🔥 ลด timeout ให้ realistic
        )

        return {
            "session_id": session_id,
            "result": result.get("final_response", ""),
            "intent": result.get("intent", "unknown"),
            "metadata": result,
        }

    except asyncio.TimeoutError:
        return {
            "session_id": session_id,
            "result": "System timeout (agent too slow)",
            "intent": "timeout",
            "metadata": {},
        }


# 🔥 FIX FRONTEND MOUNT (สำคัญ)
from fastapi.staticfiles import StaticFiles
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")