from app.agents.gmail_agent import gmail_agent
from app.agents.slack_agent import slack_agent
from app.agents.calendar_agent import calendar_agent


def run_graph(state: dict):

    text = state.get("message", "").strip().lower()

    # empty message
    if not text:
        return {
            "intent": "assistant",
            "message": "Please enter a command. Example: read email"
        }

    # greeting
    if text in ["hi", "hello", "hey"]:
        return {
            "intent": "assistant",
            "message": (
                "👋 Welcome to AI Automation Hub\n\n"
                "Available commands:\n\n"
                "📧 read email\n"
                "📧 summarize email\n"
                "📧 read email and notify slack\n"
                "📅 schedule meeting\n"
                "📧 read email and schedule meeting\n"
                "🚀 do everything"
            )
        }

    steps = []

    # email keywords
    if any(k in text for k in [
        "email",
        "gmail",
        "inbox",
        "mail",
        "check email",
        "read email",
        "summarize email"
    ]):
        steps.append("gmail")

    # slack keywords
    if any(k in text for k in [
        "slack",
        "notify",
        "send slack"
    ]):
        steps.append("slack")

    # calendar keywords
    if any(k in text for k in [
        "calendar",
        "schedule",
        "meeting",
        "appointment"
    ]):
        steps.append("calendar")

    # everything
    if any(k in text for k in [
        "everything",
        "do everything",
        "run everything"
    ]):
        steps = ["gmail", "slack", "calendar"]

    # no intent detected
    if not steps:
        return {
            "intent": "assistant",
            "message": (
                f"🤔 I don't understand: '{text}'\n\n"
                "Try:\n"
                "- read email\n"
                "- summarize email\n"
                "- notify slack\n"
                "- schedule meeting\n"
                "- do everything"
            )
        }

    result = {
        "intent": "multi_agent_task",
        "steps": steps,
        "data": {}
    }

    if "gmail" in steps:
        result["data"]["gmail"] = gmail_agent(text)

    if "slack" in steps:
        result["data"]["slack"] = slack_agent(text)

    if "calendar" in steps:
        result["data"]["calendar"] = calendar_agent(text)

    return result