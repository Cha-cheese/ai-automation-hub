from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

from app.agents.email_agent import email_node
from app.agents.calendar_agent import calendar_node
from app.agents.search_agent import search_node
from app.agents.slack_agent import slack_node
from app.agents.summarizer_agent import summarizer_node


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


def route(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    text = state["user_input"].lower()

    if "email" in text:
        return "email"
    if "meeting" in text or "schedule" in text:
        return "calendar"
    if "search" in text or "news" in text:
        return "search"

    return "general"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("email", email_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("search", search_node)
    graph.add_node("slack", slack_node)
    graph.add_node("summarizer", summarizer_node)

    graph.set_entry_point("email")

    graph.add_conditional_edges("email", route, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": "summarizer"
    })

    graph.add_edge("calendar", "slack")
    graph.add_edge("search", "slack")
    graph.add_edge("summarizer", "slack")
    graph.add_edge("slack", END)

    return graph.compile()


automation_graph = build_graph()