from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.llm import build_gemini_llm, clean_json_response, safe_json_load
from app.core.config import get_settings

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

SYSTEM_ROUTER = """Return JSON: {"intent": "process_email | schedule_meeting | web_search | general_query"}"""

def router_node(state: AgentState) -> AgentState:
    llm = build_gemini_llm(256)
    res = llm.invoke([
        SystemMessage(content=SYSTEM_ROUTER),
        HumanMessage(content=state["user_input"])
    ])

    data = safe_json_load(clean_json_response(res.content))
    return {**state, "intent": data.get("intent", "general_query")}

def route(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    return {
        "process_email": "email",
        "schedule_meeting": "calendar",
        "web_search": "search"
    }.get(state["intent"], "general")

def general_node(state: AgentState) -> AgentState:
    llm = build_gemini_llm(512)
    res = llm.invoke([HumanMessage(content=state["user_input"])])
    return {**state, "final_response": res.content}

def build_graph():
    g = StateGraph(AgentState)

    from app.agents.email_agent import email_node
    from app.agents.calendar_agent import calendar_node
    from app.agents.search_agent import search_node

    g.add_node("router", router_node)
    g.add_node("email", email_node)
    g.add_node("calendar", calendar_node)
    g.add_node("search", search_node)
    g.add_node("general", general_node)

    g.set_entry_point("router")

    g.add_conditional_edges("router", route, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": "general"
    })

    g.add_edge("email", END)
    g.add_edge("calendar", END)
    g.add_edge("search", END)
    g.add_edge("general", END)

    return g.compile()

automation_graph = build_graph()