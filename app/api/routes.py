from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
from upstash_redis import Redis
from app.core.config import get_settings
import uuid, json
from datetime import datetime

settings = get_settings()
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
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

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
        result = automation_graph.invoke(initial_state)
        redis.setex(f"session:{session_id}", 3600, json.dumps({
            "input": req.message,
            "intent": result.get("intent"),
            "response": result.get("final_response"),
            "timestamp": datetime.now().isoformat(),
        }))
        return AutomationResponse(
            session_id=session_id,
            result=result.get("final_response", "Done"),
            intent=result.get("intent", "unknown"),
            metadata={
                "slack_sent": result.get("slack_sent"),
                "calendar_event": result.get("calendar_event", {}).get("id"),
                "search_count": len(result.get("search_results", [])),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    data = redis.get(f"session:{session_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Session not found")
    return json.loads(data)

try:
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
except:
    pass
