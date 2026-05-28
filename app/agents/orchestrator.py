from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from app.agents.llm import build_gemini_llm

class AgentState(TypedDict):
    user_input: str
    intent: str
    final_response: str

def router_node(state: AgentState):
    text = state["user_input"].lower()

    if any(x in text for x in ["email", "gmail"]):
        intent = "email"
    elif any(x in text for x in ["meeting", "calendar", "schedule"]):
        intent = "calendar"
    elif any(x in text for x in ["search", "news"]):
        intent = "search"
    elif "slack" in text:
        intent = "slack"
    else:
        intent = "general"

    return {**state, "intent": intent}

def route(state: AgentState):
    return state["intent"]

# 🔥 REAL LLM NODE (FIXED)
def general_node(state: AgentState):

    llm = build_gemini_llm(max_tokens=512)

    response = llm.invoke([
        HumanMessage(content=state["user_input"])
    ])

    return {
        **state,
        "final_response": response.content
    }

from app.agents.email_agent import email_node
from app.agents.calendar_agent import calendar_node
from app.agents.search_agent import search_node
from app.agents.slack_agent import slack_node

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("email", email_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("search", search_node)
    graph.add_node("slack", slack_node)
    graph.add_node("general", general_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges("router", route, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "slack": "slack",
        "general": "general",
    })

    graph.add_edge("email", END)
    graph.add_edge("calendar", END)
    graph.add_edge("search", END)
    graph.add_edge("slack", END)
    graph.add_edge("general", END)

    return graph.compile()

automation_graph = build_graph()