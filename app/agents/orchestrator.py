from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

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


def route(state: AgentState) -> Literal["email", "calendar", "search", "slack", "general"]:
    intent = state.get("intent", "general")
    return intent if intent in ["email", "calendar", "search"] else "general"


def general_node(state: AgentState):
    return {**state, "final_response": f"AI Hub: {state['user_input']}"}


def build_graph():
    g = StateGraph(AgentState)

    from app.agents.email_agent import email_node
    from app.agents.calendar_agent import calendar_node
    from app.agents.search_agent import search_node
    from app.agents.slack_agent import slack_node

    g.add_node("email", email_node)
    g.add_node("calendar", calendar_node)
    g.add_node("search", search_node)
    g.add_node("general", general_node)

    g.set_entry_point("general")

    g.add_conditional_edges("general", route, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": END
    })

    g.add_edge("email", END)
    g.add_edge("calendar", END)
    g.add_edge("search", END)

    return g.compile()

automation_graph = build_graph()