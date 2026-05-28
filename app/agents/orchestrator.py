from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
from app.agents.email_agent import email_node
from app.agents.calendar_agent import calendar_node
from app.agents.search_agent import search_node
from app.agents.slack_agent import slack_node
from app.agents.llm import build_gemini_llm, safe_json_load
from langchain_core.messages import HumanMessage, SystemMessage

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


def router(state: AgentState):
    try:
        llm = build_gemini_llm(max_tokens=200)

        res = llm.invoke([
            SystemMessage(content="Return JSON: intent = email/calendar/search/general"),
            HumanMessage(content=state["user_input"])
        ])

        parsed = safe_json_load(res.content)

        return {**state, "intent": parsed.get("intent", "general")}
    except:
        return {**state, "intent": "general"}


def route(state: AgentState) -> Literal["email","calendar","search","general"]:
    return state.get("intent", "general")


def general_node(state: AgentState):
    return {**state, "final_response": f"AI Automation Hub received: {state['user_input']}"}


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("router", router)
    g.add_node("email", email_node)
    g.add_node("calendar", calendar_node)
    g.add_node("search", search_node)
    g.add_node("slack", slack_node)
    g.add_node("general", general_node)

    g.set_entry_point("router")

    g.add_conditional_edges("router", route, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": "general",
    })

    g.add_edge("email", "slack")
    g.add_edge("calendar", END)
    g.add_edge("search", END)
    g.add_edge("slack", END)
    g.add_edge("general", END)

    return g.compile()

automation_graph = build_graph()