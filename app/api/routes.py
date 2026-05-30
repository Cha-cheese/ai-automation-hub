from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.graph import run_graph
from app.core.formatter import format_response

router = APIRouter()


class AutomateReq(BaseModel):
    message: str


@router.post("/automate")
def automate(req: AutomateReq):

    result = run_graph({
        "message": req.message
    })

    return {
        "status": "success",
        "result": format_response(result)
    }