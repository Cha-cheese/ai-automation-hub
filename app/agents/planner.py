import json

def planner_agent(user_input: str):

    text = user_input.lower()

    steps = []

    if "email" in text or "read" in text:
        steps.append("gmail")

    if "slack" in text or "notify" in text:
        steps.append("slack")

    if "schedule" in text or "meeting" in text:
        steps.append("calendar")

    if not steps:
        steps = ["gmail"]

    return {"steps": steps}