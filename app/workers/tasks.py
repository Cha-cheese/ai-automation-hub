from app.core.celery_app import celery
from app.agents.orchestrator import automation_graph


@celery.task
def run_agent_task(session_id: str, message: str):
    state = {
        "user_input": message,
        "intent": None,
        "final_response": ""
    }

    result = automation_graph.invoke(state)

    return {
        "session_id": session_id,
        "result": result.get("final_response"),
        "intent": result.get("intent")
    }