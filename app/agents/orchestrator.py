from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import get_settings
import json

settings = get_settings()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=settings.google_api_key,
    max_tokens=1024,
)

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

SYSTEM_ROUTER = """You are a routing agent. Analyze the user's request and return a JSON object with:
- "intent": one of ["process_email", "schedule_meeting", "web_search", "general_query"]
- "details": extracted key information

Respond ONLY with valid JSON, no markdown, no explanation."""

def router_node(state: AgentState) -> AgentState:
    response = llm.invoke([
        SystemMessage(content=SYSTEM_ROUTER),
        HumanMessage(content=state["user_input"])
    ])
    try:
        text = response.content.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        parsed = json.loads(text.strip())
        return {**state, "intent": parsed.get("intent", "general_query")}
    except:
        return {**state, "intent": "general_query"}

def route_by_intent(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    intent_map = {
        "process_email": "email",
        "schedule_meeting": "calendar",
        "web_search": "search",
        "general_query": "general",
    }
    return intent_map.get(state["intent"], "general")

def general_node(state: AgentState) -> AgentState:
    response = llm.invoke([HumanMessage(content=state["user_input"])])
    return {**state, "final_response": response.content}

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("router", router_node)
    graph.add_node("general", general_node)

    from app.agents.email_agent import email_node
    from app.agents.summarizer_agent import summarizer_node
    from app.agents.slack_agent import slack_node
    from app.agents.calendar_agent import calendar_node
    from app.agents.search_agent import search_node

    graph.add_node("email", email_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("slack", slack_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("search", search_node)

    graph.set_entry_point("router")
    graph.add_conditional_edges("router", route_by_intent, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": "general",
    })
    graph.add_edge("email", "summarizer")
    graph.add_edge("summarizer", "slack")
    graph.add_edge("slack", END)
    graph.add_edge("calendar", END)
    graph.add_edge("search", END)
    graph.add_edge("general", END)

    return graph.compile()

automation_graph = build_graph()