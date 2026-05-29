from fastapi import FastAPI, Header
from pydantic import BaseModel

from app.agents.orchestrator import automation_graph
from app.core.auth import verify_token

app = FastAPI()


class AutomateReq(BaseModel):
    message: str


@app.post("/automate")
def automate(req: AutomateReq, authorization: str = Header(None)):

    try:

        if not authorization:
            return {"error": "missing token"}

        user = verify_token(authorization)

        if not user:
            return {"error": "unauthorized"}

        result = automation_graph({
            "user_input": req.message
        })

        return result

    except Exception as e:

        return {
            "error": "internal_error",
            "detail": str(e)
        }