from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.llm import build_gemini_llm, clean_json_response
from app.core.config import get_settings
from app.core.errors import safe_error_message
import json

settings = get_settings()

class AgentState(TypedDict):
    user_input: str
    intent: str
    final_response: str
    error: str

SYSTEM_ROUTER = """
Return JSON only:
{
 "intent": "email|calendar|search|general"
}
"""

def router_node(state: AgentState):
    try:
        llm = build_gemini_llm(128)
        res = llm.invoke([
            SystemMessage(content=SYSTEM_ROUTER),
            HumanMessage(content=state["user_input"])
        ])
        data = json.loads(clean_json_response(res.content))
        return {**state, "intent": data.get("intent", "general")}
    except Exception as e:
        return {**state, "intent": "general", "error": str(e)}

def general_node(state: AgentState):
    try:
        llm = build_gemini_llm(256)
        res = llm.invoke([HumanMessage(content=state["user_input"])])
        return {**state, "final_response": res.content}
    except Exception as e:
        return {
            **state,
            "final_response": "Fallback response (Gemini error)",
            "error": str(e)
        }

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("general", general_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        lambda s: s["intent"],
        {
            "general": "general",
            "email": "general",
            "calendar": "general",
            "search": "general",
        },
    )

    graph.add_edge("general", END)

    return graph.compile()

automation_graph = build_graph()