from fastapi import FastAPI, Header
from pydantic import BaseModel
from app.agents.orchestrator import automation_graph
from app.core.auth import login as auth_login, verify_token

app = FastAPI()


# ---------- MODELS ----------
class LoginReq(BaseModel):
    username: str
    password: str


class AutomateReq(BaseModel):
    message: str


# ---------- ROUTES ----------
@app.get("/")
def root():
    return {"status": "AI Automation Hub running"}


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