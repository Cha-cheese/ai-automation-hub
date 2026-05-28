from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
import uuid, asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Req(BaseModel):
    message: str
    session_id: str = None

@app.post("/automate")
async def automate(req: Req):
    session_id = req.session_id or str(uuid.uuid4())

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
                "error": ""
            }),
            timeout=40
        )

        return {
            "session_id": session_id,
            "result": result.get("final_response"),
            "intent": result.get("intent")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))