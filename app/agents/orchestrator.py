from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal


from app.agents.email_agent import email_node
from app.agents.calendar_agent import calendar_node
from app.agents.search_agent import search_node
from app.agents.slack_agent import slack_node
from app.agents.summarizer_agent import summarizer_node


class AgentState(TypedDict):
    user_input: str
    intent: str | None
    email_data: dict | None
    summary: str | None
    category: str | None
    slack_sent: bool
    calendar_event: dict | None
    search_results: list
    final_response: str
    error: str | None


# 🔥 LEVEL 4 INTENT CLASSIFIER (FIXED)
def classify_intent(state: AgentState) -> str:
    text = state["user_input"].lower()

    if any(k in text for k in ["email", "gmail", "inbox"]):
        return "email"

    if any(k in text for k in ["meeting", "schedule", "calendar"]):
        return "calendar"

    if any(k in text for k in ["search", "news", "google"]):
        return "search"

    return "general"


def route(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    return classify_intent(state)


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