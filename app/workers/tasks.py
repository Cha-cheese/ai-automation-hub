from app.core.queue import celery
from app.agents.orchestrator import automation_graph


@celery.task
def run_ai(user_input, user_id):

    result = automation_graph({
        "user_input": user_input,
        "user_id": user_id
    })

    return result