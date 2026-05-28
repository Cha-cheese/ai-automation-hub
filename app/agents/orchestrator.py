from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def automation_graph(state):

    user_input = state["user_input"]
    memory = state.get("memory", {})

    prompt = f"""
You are an AI automation agent.

Previous memory:
{memory}

User request:
{user_input}

Return a helpful response.
"""

    response = llm.invoke(prompt)

    state["final_response"] = str(response)
    state["intent"] = "processed"

    return state