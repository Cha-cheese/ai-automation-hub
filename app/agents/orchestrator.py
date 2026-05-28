from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def automation_graph(state):

    try:
        user_input = state.get("user_input", "")

        prompt = f"""
You are an AI assistant.

User request:
{user_input}

Return simple response.
"""

        response = llm.invoke(prompt)

        return {
            "final_response": str(response),
            "intent": "ok"
        }

    except Exception as e:
        return {
            "final_response": "AI error",
            "error": str(e),
            "intent": "failed"
        }