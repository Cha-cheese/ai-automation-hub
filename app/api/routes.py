from fastapi import FastAPI, Header
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
from app.core.auth import login as auth_login, verify_token
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

FRONTEND_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "frontend"
)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# ---------- MODELS ----------
class LoginReq(BaseModel):
    username: str
    password: str


class AutomateReq(BaseModel):
    message: str


# ---------- ROUTES ----------
@app.get("/")
def root():
    return FileResponse(
        os.path.join(FRONTEND_DIR, "index.html")
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/login")
def login_api(req: LoginReq):
    token = auth_login(req.username, req.password)

    if not token:
        return {"error": "invalid credentials"}

    return {"token": token}


@app.post("/automate")
def automate(req: AutomateReq, authorization: str = Header(None)):

    user = verify_token(authorization)

    if not user:
        return {"error": "unauthorized"}

    result = automation_graph({
        "user_input": req.message
    })

    return {
        "result": result.get("final_response"),
        "intent": result.get("intent")
    }