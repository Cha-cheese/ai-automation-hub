from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.agents.orchestrator import automation_graph

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


@app.get("/health")
def health():
    return {"status": "ok"}