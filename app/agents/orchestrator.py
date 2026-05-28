from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.llm import build_gemini_llm
from app.core.config import get_settings
from app.core.errors import safe_error_message
import json

settings = get_settings()

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


def router_node(state: AgentState) -> AgentState:
    text = state["user_input"].lower()

    if any(x in text for x in ["email", "mail"]):
        intent = "process_email"
    elif any(x in text for x in ["meeting", "schedule", "calendar", "นัด"]):
        intent = "schedule_meeting"
    elif any(x in text for x in ["search", "news", "ค้นหา"]):
        intent = "web_search"
    else:
        intent = "general_query"

    return {**state, "intent": intent}


def route_by_intent(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    return {
        "process_email": "email",
        "schedule_meeting": "calendar",
        "web_search": "search",
    }.get(state["intent"], "general")


def general_node(state: AgentState) -> AgentState:
    try:
        llm = build_gemini_llm(max_tokens=200)

        response = llm.invoke([
            HumanMessage(content=state["user_input"])
        ])

        return {**state, "final_response": response.content}

    except Exception as e:
        return {
            **state,
            "final_response": f"AI Hub: {state['user_input']}",
            "error": safe_error_message(e)
        }


def build_graph():
    graph = StateGraph(AgentState)

    from app.agents.email_agent import email_node
    from app.agents.calendar_agent import calendar_node
    from app.agents.search_agent import search_node

    graph.add_node("router", router_node)
    graph.add_node("email", email_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("search", search_node)
    graph.add_node("general", general_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges("router", route_by_intent, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": "general",
    })

    graph.add_edge("email", END)
    graph.add_edge("calendar", END)
    graph.add_edge("search", END)
    graph.add_edge("general", END)

    return graph.compile()

automation_graph = build_graph()