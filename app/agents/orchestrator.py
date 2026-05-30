from app.agents.planner import plan_route
from app.agents.gmail_agent import email_agent
from app.agents.slack_agent import slack_agent
from app.agents.calendar_agent import calendar_agent
from app.agents.web_agent import web_agent


def automation_graph(state):

    user_input = state.get("user_input", "")

    # 🧠 Step 1: Planner decides route
    plan = plan_route(user_input)

    result = {
        "intent": plan["intent"],
        "steps": plan["steps"],
        "data": {}
    }

    # 📧 EMAIL
    if "email" in plan["steps"]:
        result["data"]["email"] = email_agent(user_input)

    # 💬 SLACK
    if "slack" in plan["steps"]:
        result["data"]["slack"] = slack_agent(user_input)

    # 📅 CALENDAR
    if "calendar" in plan["steps"]:
        result["data"]["calendar"] = calendar_agent(user_input)

    # 🌐 WEB
    if "web" in plan["steps"]:
        result["data"]["web"] = web_agent(user_input)

    return result