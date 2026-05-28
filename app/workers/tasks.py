from app.core.celery_app import celery
from app.agents.orchestrator import automation_graph


@celery.task
def run_automation(message: str):

    state = {
        "user_input": message,
        "intent": "",
        "final_response": ""
    }

    result = automation_graph.invoke(state)

    return {
        "result": result.get("final_response"),
        "intent": result.get("intent")
    }