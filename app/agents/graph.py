from app.agents.gmail_agent import gmail_agent
from app.agents.slack_agent import slack_agent
from app.agents.calendar_agent import calendar_agent

def run_graph(state: dict):

    text = state.get("message", "").lower()

    steps = []

    if "gmail" in text or "email" in text:
        steps.append("gmail")

    if "slack" in text:
        steps.append("slack")

    if "calendar" in text or "schedule" in text:
        steps.append("calendar")

    if "everything" in text or "do everything" in text:
        steps = ["gmail", "slack", "calendar"]

    result = {"intent": "multi_agent_task", "steps": steps, "data": {}}

    if "gmail" in steps:
        result["data"]["gmail"] = gmail_agent(text)

    if "slack" in steps:
        result["data"]["slack"] = slack_agent(text)

    if "calendar" in steps:
        result["data"]["calendar"] = calendar_agent(text)

    return result