from app.agents.llm import build_gemini_llm

# 🧠 SAFE IMPORT (กัน deploy crash)
try:
    from langgraph.graph import StateGraph, END
    HAS_LANGGRAPH = True
except Exception:
    StateGraph = None
    END = None
    HAS_LANGGRAPH = False


llm = build_gemini_llm()


# -------------------------
# 🧠 SAFE UTIL
# -------------------------
def safe_llm(prompt: str) -> str:
    try:
        res = llm.invoke(prompt)
        return str(res)
    except Exception as e:
        return f"LLM_ERROR: {str(e)}"


# -------------------------
# 🧠 AGENTS
# -------------------------
def planner(state):
    user_input = state.get("user_input", "")

    prompt = f"""
You are a planner agent.
Break this task into steps:

{user_input}
"""

    plan = safe_llm(prompt)

    return {
        **state,
        "plan": plan,
        "intent": "planned"
    }


def executor(state):
    plan = state.get("plan", "")

    prompt = f"""
Execute this plan step by step:

{plan}
"""

    result = safe_llm(prompt)

    return {
        **state,
        "result": result,
        "intent": "executed"
    }


def reviewer(state):
    result = state.get("result", "")

    prompt = f"""
Review and improve this output:

{result}
"""

    review = safe_llm(prompt)

    return {
        **state,
        "final_response": review,
        "intent": "completed"
    }


# -------------------------
# 🧠 GRAPH BUILDER (SAFE)
# -------------------------
def build_graph():

    # fallback mode ถ้าไม่มี langgraph
    if not HAS_LANGGRAPH:
        def fallback(state):
            state = planner(state)
            state = executor(state)
            state = reviewer(state)
            return state

        return fallback

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