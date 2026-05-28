import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from app.workers.tasks import run_agent_task

app = FastAPI()

class Req(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "LEVEL 6 AI Automation Platform"}


@app.post("/automate")
def automate(req: Req):
    session_id = str(uuid.uuid4())

    task = run_agent_task.delay(session_id, req.message)

    return {
        "session_id": session_id,
        "task_id": task.id,
        "status": "queued"
    }


from app.core.celery_app import celery

@app.get("/result/{task_id}")
def get_result(task_id: str):
    result = celery.AsyncResult(task_id)

    if result.ready():
        return {
            "status": "done",
            "data": result.get()
        }

    return {
        "status": "processing"
    }

from langgraph.graph import StateGraph, END
from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def general_node(state):
    res = llm.invoke(state["user_input"])
    return {**state, "final_response": str(res), "intent": "general"}


def build_graph():
    graph = StateGraph(dict)

    graph.add_node("general", general_node)
    graph.set_entry_point("general")

    graph.add_edge("general", END)

    return graph.compile()


automation_graph = build_graph()
