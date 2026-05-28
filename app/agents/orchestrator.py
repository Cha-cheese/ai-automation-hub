from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from datetime import datetime, timedelta
import re

class AgentState(TypedDict):
    user_input: str
    intent: str
    email_data: dict
    summary: str
    category: str
    slack_sent: bool
    calendar_event: dict
    search_results: list
    final_response: str
    error: str

def detect_intent(text: str) -> str:
    t = text.lower()

    if any(x in t for x in ["email", "gmail", "inbox", "mail"]):
        return "process_email"

    if any(x in t for x in ["meeting", "schedule", "calendar", "appointment"]):
        return "schedule_meeting"

    if any(x in t for x in ["search", "latest", "news", "research"]):
        return "web_search"

    return "general_query"

def router_node(state: AgentState) -> AgentState:
    intent = detect_intent(state["user_input"])
    return {**state, "intent": intent}

def route_by_intent(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    mapping = {
        "process_email": "email",
        "schedule_meeting": "calendar",
        "web_search": "search",
        "general_query": "general",
    }
    return mapping.get(state["intent"], "general")

def general_node(state: AgentState) -> AgentState:
    text = state["user_input"]

    return {
        **state,
        "final_response": f"AI Automation Hub received: {text}"
    }

def email_node(state: AgentState) -> AgentState:
    emails = [
        {
            "from": "Google",
            "subject": "Security Alert",
            "snippet": "A new login was detected."
        },
        {
            "from": "LeetCode",
            "subject": "New Contest",
            "snippet": "Join this week's coding contest."
        }
    ]

    summary = (
        "📧 Gmail Summary:\n"
        "- Google sent a security notification\n"
        "- LeetCode announced a new coding contest"
    )

    return {
        **state,
        "email_data": {"emails": emails},
        "summary": summary,
        "final_response": summary
    }

def calendar_node(state: AgentState) -> AgentState:
    text = state["user_input"]

    tomorrow = datetime.now() + timedelta(days=1)

    event = {
        "title": text,
        "time": tomorrow.strftime("%Y-%m-%d 15:00")
    }

    return {
        **state,
        "calendar_event": event,
        "final_response": f"✅ Meeting scheduled for {event['time']}"
    }

def search_node(state: AgentState) -> AgentState:
    query = state["user_input"]

    results = [
        "Germany increases AI investment in 2026.",
        "European companies adopt multi-agent automation systems.",
        "LangGraph and AI workflow orchestration continue growing."
    ]

    response = "🔍 Search Results:\n\n"

    for r in results:
        response += f"- {r}\n"

    return {
        **state,
        "search_results": results,
        "final_response": response
    }

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("general", general_node)
    graph.add_node("email", email_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("search", search_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        route_by_intent,
        {
            "email": "email",
            "calendar": "calendar",
            "search": "search",
            "general": "general",
        }
    )

    graph.add_edge("email", END)
    graph.add_edge("calendar", END)
    graph.add_edge("search", END)
    graph.add_edge("general", END)

    return graph.compile()

automation_graph = build_graph()