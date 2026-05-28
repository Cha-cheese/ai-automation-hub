from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.llm import build_gemini_llm, clean_json_response
from app.core.config import get_settings
from app.core.errors import safe_error_message
import json
from langchain_google_genai import ChatGoogleGenerativeAI

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

SYSTEM_ROUTER = """You are a routing agent. Analyze the user's request and return a JSON object with:
- "intent": one of ["process_email", "schedule_meeting", "web_search", "general_query"]
- "details": extracted key information

Respond ONLY with valid JSON, no markdown, no explanation."""

def heuristic_intent(user_input: str) -> str:
    text = user_input.lower()
    if any(word in text for word in ["email", "gmail", "inbox", "mail"]):
        return "process_email"
    if any(word in text for word in ["meeting", "schedule", "calendar", "appointment", "นัด", "ประชุม"]):
        return "schedule_meeting"
    if any(word in text for word in ["search", "latest", "news", "research", "ค้นหา", "ข่าว"]):
        return "web_search"
    return "general_query"

def router_node(state: AgentState) -> AgentState:
    heuristic = heuristic_intent(state["user_input"])
    if heuristic != "general_query":
        return {**state, "intent": heuristic}

    try:
        llm = build_gemini_llm(max_tokens=256)
        response = llm.invoke([
            SystemMessage(content=SYSTEM_ROUTER),
            HumanMessage(content=state["user_input"])
        ])
        parsed = json.loads(clean_json_response(response.content))
        return {**state, "intent": parsed.get("intent", "general_query")}
    except Exception as e:
        return {**state, "intent": heuristic, "error": safe_error_message(e)}

def route_by_intent(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    intent_map = {
        "process_email": "email",
        "schedule_meeting": "calendar",
        "web_search": "search",
        "general_query": "general",
    }
    return intent_map.get(state["intent"], "general")

def general_node(state: AgentState) -> AgentState:
    if settings.demo_mode:
        return {
            **state,
            "final_response": (
                "Demo assistant response: I can route requests to email processing, calendar scheduling, "
                "Slack notifications, and web research. Try one of the example chips above."
            ),
        }

    try:
        llm = build_gemini_llm(max_tokens=512)
        response = llm.invoke([HumanMessage(content=state["user_input"])])
        return {**state, "final_response": response.content}
    except Exception as e:
        return {
            **state,
            "error": safe_error_message(e),
            "final_response": (
                "Demo mode response: the router understood your request, but Gemini is not available. "
                "Set GOOGLE_API_KEY in the environment and redeploy to enable live AI responses."
            ),
        }

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
