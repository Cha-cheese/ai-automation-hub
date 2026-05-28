from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def automation_graph(state):

    prompt = f"""
You are an AI automation system.

User request:
{state["user_input"]}

Return structured response.
"""

    response = llm.invoke(prompt)

    return {
        "final_response": str(response),
        "intent": "processed"
    }