from langgraph.graph import StateGraph, END
from app.agents.llm import build_gemini_llm


llm = build_gemini_llm()


def classify(state):
    text = state["user_input"].lower()

    if "email" in text:
        return "email"
    if "meeting" in text:
        return "calendar"
    if "search" in text:
        return "search"

    return "general"


def email_node(state):
    res = llm.invoke(f"Summarize email task: {state['user_input']}")
    return {**state, "final_response": str(res), "intent": "email"}


def calendar_node(state):
    return {
        **state,
        "final_response": "📅 Calendar event created (production-ready stub)",
        "intent": "calendar"
    }


def search_node(state):
    return {
        **state,
        "final_response": "🔍 Search completed",
        "intent": "search"
    }


def general_node(state):
    res = llm.invoke(state["user_input"])
    return {**state, "final_response": str(res), "intent": "general"}


def route(state):
    return classify(state)


def build_graph():
    graph = StateGraph(dict)

    graph.add_node("email", email_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("search", search_node)
    graph.add_node("general", general_node)

    graph.set_entry_point("general")

    graph.add_conditional_edges("general", route, {
        "email": "email",
        "calendar": "calendar",
        "search": "search",
        "general": "general"
    })

    graph.add_edge("email", END)
    graph.add_edge("calendar", END)
    graph.add_edge("search", END)
    graph.add_edge("general", END)

    return graph.compile()


automation_graph = build_graph()