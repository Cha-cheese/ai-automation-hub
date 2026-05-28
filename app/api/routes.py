from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.agents.orchestrator import automation_graph

app = FastAPI()

# ✅ FIX: correct base path for Render
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
def automate(req: dict):

    result = automation_graph({
        "user_input": req.get("message", "")
    })

    return {
        "result": result.get("final_response"),
        "intent": result.get("intent")
    }


# ✅ ONLY mount if folder exists (CRITICAL FIX)
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")