from fastapi import APIRouter, Header
from pydantic import BaseModel

from app.agents.orchestrator import automation_graph
from app.core.auth import login as auth_login, verify_token

router = APIRouter()


# ---------------- LOGIN ----------------
class LoginReq(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(req: LoginReq):

    token = auth_login(req.username, req.password)

    if not token:
        return {"error": "invalid credentials"}

    return {"token": token}


# ---------------- AUTOMATE ----------------
class AutomateReq(BaseModel):
    message: str


@router.post("/automate")
def automate(req: AutomateReq, authorization: str = Header(None)):

    user = verify_token(authorization)

    if not user:
        return {"error": "unauthorized"}

    result = automation_graph({
        "user_input": req.message
    })

    return result


# ---------------- HEALTH CHECK ----------------
@router.get("/")
def root():
    return {"status": "ok"}