from fastapi import FastAPI, Header
from app.workers.tasks import run_ai
from app.core.auth import verify_token
import uuid
from pydantic import BaseModel
from app.core.auth import login as auth_login

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/automate")
def automate(req, authorization: str = None):

    try:
        result = automation_graph({
            "user_input": req.message
        })

        return {
            "session_id": "ok",
            "result": result.get("final_response", str(result)),
            "intent": result.get("intent", "unknown")
        }

    except Exception as e:
        return {
            "error": "internal_error",
            "detail": str(e)
        }


@app.post("/login")
def login_api(req: LoginReq):

    token = auth_login(req.username, req.password)

    if not token:
        return {"error": "invalid credentials"}

    return {
        "token": token
    }


