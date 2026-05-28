from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Req(BaseModel):
    message: str

@app.post("/automate")
async def automate(req: Req):

    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(automation_graph.invoke, {
                "user_input": req.message,
                "intent": "",
                "final_response": ""
            }),
            timeout=40
        )

        return {
            "result": result["final_response"],
            "intent": result["intent"]
        }

    except asyncio.TimeoutError:
        return {
            "result": "System timeout - check API keys",
            "intent": "error"
        }

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")