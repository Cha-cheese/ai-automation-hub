from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
from upstash_redis import Redis
from app.core.config import get_settings
from app.core.errors import safe_error_message
import asyncio
import uuid, json
from datetime import datetime

settings = get_settings()
redis = None
if settings.upstash_redis_rest_url and settings.upstash_redis_rest_token:
    redis = Redis(url=settings.upstash_redis_rest_url, token=settings.upstash_redis_rest_token)

app = FastAPI(title="AI Automation Hub", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AutomationRequest(BaseModel):
    message: str
    session_id: str = None

class AutomationResponse(BaseModel):
    session_id: str
    result: str
    intent: str
    metadata: dict

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "2026-05-28-timeout-v2",
        "timestamp": datetime.now().isoformat(),
    }

@app.get("/debug/config")
async def debug_config():
    if settings.app_env == "production":
        return {
            "app_env": settings.app_env,
            "gemini_model": settings.gemini_model,
            "has_google_api_key": bool(settings.google_api_key),
            "has_tavily_api_key": bool(settings.tavily_api_key),
            "has_slack_bot_token": bool(settings.slack_bot_token),
            "has_google_service_account_json": settings.google_service_account_json not in ("", "{}"),
            "has_upstash_redis": bool(settings.upstash_redis_rest_url and settings.upstash_redis_rest_token),
            "request_timeout_seconds": settings.request_timeout_seconds,
            "llm_timeout_seconds": settings.llm_timeout_seconds,
            "tavily_timeout_seconds": settings.tavily_timeout_seconds,
        }
    return settings.model_dump(exclude={"google_api_key", "tavily_api_key", "slack_bot_token", "upstash_redis_rest_token"})

@app.post("/automate", response_model=AutomationResponse)
async def automate(req: AutomationRequest):
    session_id = req.session_id or str(uuid.uuid4())
    try:
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
        result = await asyncio.wait_for(
            asyncio.to_thread(automation_graph.invoke, initial_state),
            timeout=settings.request_timeout_seconds,
        )

        if redis:
            try:
                redis.setex(f"session:{session_id}", 3600, json.dumps({
                    "input": req.message,
                    "intent": result.get("intent"),
                    "response": result.get("final_response"),
                    "timestamp": datetime.now().isoformat(),
                }))
            except Exception:
                pass

        return AutomationResponse(
            session_id=session_id,
            result=result.get("final_response", "Done"),
            intent=result.get("intent", "unknown"),
            metadata={
                "slack_sent": result.get("slack_sent"),
                "calendar_event": result.get("calendar_event", {}).get("id"),
                "search_count": len(result.get("search_results", [])),
                "error": safe_error_message(result.get("error", "")),
            }
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"Automation timed out after {settings.request_timeout_seconds} seconds. Check external API keys/network latency.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=safe_error_message(e))

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    if not redis:
        raise HTTPException(status_code=503, detail="Redis is not configured")
    data = redis.get(f"session:{session_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Session not found")
    return json.loads(data)

try:
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
except:
    pass
