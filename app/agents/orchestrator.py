from langgraph.graph import StateGraph, END
from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


# 🧠 PLANNER AGENT
def planner(state):
    prompt = f"""
    You are a planner agent.
    Break this task into steps:

    {state['user_input']}
    """

    plan = llm.invoke(prompt)

    return {
        **state,
        "plan": str(plan),
        "intent": "planned"
    }


# ⚙️ EXECUTOR AGENT
def executor(state):
    prompt = f"""
    Execute this plan:
    {state.get('plan')}
    """

    result = llm.invoke(prompt)

    return {
        **state,
        "result": str(result),
        "intent": "executed"
    }


# 🧪 REVIEW AGENT
def reviewer(state):
    prompt = f"""
    Review this output and improve if needed:
    {state.get('result')}
    """

    review = llm.invoke(prompt)

    return {
        **state,
        "final_response": str(review),
        "intent": "completed"
    }


def build_graph():
    graph = StateGraph(dict)

    graph.add_node("planner", planner)
    graph.add_node("executor", executor)
    graph.add_node("reviewer", reviewer)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "reviewer")
    graph.add_edge("reviewer", END)

    return graph.compile()


automation_graph = build_graph()