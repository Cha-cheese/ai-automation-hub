from fastapi import APIRouter
from pydantic import BaseModel

from app.core.auth import login as auth_login

router = APIRouter()


# ---------- LOGIN REQUEST MODEL ----------
class LoginReq(BaseModel):
    username: str
    password: str


# ---------- LOGIN ROUTE ----------
@router.post("/login")
def login(req: LoginReq):

    token = auth_login(req.username, req.password)

    if not token:
        return {
            "error": "invalid credentials"
        }

    return {
        "token": token
    }