from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
from app.agents.llm import build_gemini_llm

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


# 🔥 FAST ROUTER (NO AI)
def router(state: AgentState):
    text = state["user_input"].lower()

    if any(k in text for k in ["email", "gmail"]):
        intent = "email"
    elif any(k in text for k in ["meeting", "calendar", "schedule"]):
        intent = "calendar"
    elif any(k in text for k in ["search", "news"]):
        intent = "search"
    else:
        intent = "general"

    return {**state, "intent": intent}


def route(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    return state["intent"]


def general_node(state: AgentState):
    return {
        **state,
        "final_response": f"AI Hub: {state['user_input']}"
    }


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("router", router)
    g.add_node("email", lambda s: {**s, "final_response": "Email processed (async safe mode)"})
    g.add_node("calendar", lambda s: {**s, "final_response": "Calendar event created (mock safe mode)"})
    g.add_node("search", lambda s: {**s, "final_response": "Search completed (fast mode)"})
    g.add_node("general", general_node)

    g.set_entry_point("router")

    g.add_conditional_edges("router", route, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": "general",
    })

    g.add_edge("email", END)
    g.add_edge("calendar", END)
    g.add_edge("search", END)
    g.add_edge("general", END)

    return g.compile()

automation_graph = build_graph()