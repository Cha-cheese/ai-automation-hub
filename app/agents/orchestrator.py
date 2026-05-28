from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def planner(state):
    prompt = f"Plan this: {state['user_input']}"
    plan = llm.invoke(prompt)
    state["plan"] = str(plan)
    state["intent"] = "planned"
    return state


def executor(state):
    prompt = f"Execute this plan: {state.get('plan')}"
    result = llm.invoke(prompt)
    state["result"] = str(result)
    state["intent"] = "executed"
    return state


def reviewer(state):
    prompt = f"Improve this result: {state.get('result')}"
    final = llm.invoke(prompt)
    state["final_response"] = str(final)
    state["intent"] = "completed"
    return state


def automation_graph(state: dict):

    state = planner(state)
    state = executor(state)
    state = reviewer(state)

    return state