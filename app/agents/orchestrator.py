from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

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

def heuristic_intent(user_input: str) -> str:
    text = user_input.lower()

    if any(word in text for word in ["email", "gmail", "inbox"]):
        return "process_email"

    if any(word in text for word in ["meeting", "schedule", "calendar"]):
        return "schedule_meeting"

    if any(word in text for word in ["search", "news", "latest"]):
        return "web_search"

    return "general_query"

def router_node(state: AgentState) -> AgentState:
    intent = heuristic_intent(state["user_input"])
    return {**state, "intent": intent}

def route_by_intent(state: AgentState) -> Literal["email", "calendar", "search", "general"]:
    mapping = {
        "process_email": "email",
        "schedule_meeting": "calendar",
        "web_search": "search",
        "general_query": "general",
    }

    return mapping.get(state["intent"], "general")

def general_node(state: AgentState) -> AgentState:
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key="YOUR_GOOGLE_API_KEY",
            temperature=0.3,
        )

        response = llm.invoke([
            HumanMessage(content=state["user_input"])
        ])

        return {
            **state,
            "final_response": response.content
        }

    except Exception as e:
        return {
            **state,
            "final_response": f"Gemini error: {str(e)}"
        }

def email_node(state: AgentState) -> AgentState:
    return {
        **state,
        "final_response": "Checked Gmail successfully (mock)."
    }

def calendar_node(state: AgentState) -> AgentState:
    return {
        **state,
        "final_response": "Meeting scheduled successfully (mock)."
    }

def search_node(state: AgentState) -> AgentState:
    return {
        **state,
        "final_response": "Web search completed successfully (mock)."
    }

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("general", general_node)
    graph.add_node("email", email_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("search", search_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges("router", route_by_intent, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": "general",
    })

    graph.add_edge("general", END)
    graph.add_edge("email", END)
    graph.add_edge("calendar", END)
    graph.add_edge("search", END)

    return graph.compile()

automation_graph = build_graph()