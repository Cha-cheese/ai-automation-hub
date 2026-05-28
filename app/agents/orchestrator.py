from app.agents.llm import build_gemini_llm
from app.tools.slack import send_slack

llm = build_gemini_llm()


def automation_graph(state):

    user_input = state["user_input"]

    prompt = f"""
You are an AI automation assistant.

User: {user_input}
Memory: {state.get("memory")}

Return helpful response.
"""

    response = llm.invoke(prompt)

    # auto slack notify (demo product behavior)
    if "slack" in user_input.lower():
        send_slack(str(response))

    state["final_response"] = str(response)
    state["intent"] = "processed"

    return state