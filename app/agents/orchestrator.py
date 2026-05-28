from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def automation_graph(state):
    try:
        prompt = f"""
User request:
{state.get("user_input", "")}
"""

        response = llm.invoke(prompt)

        return {
            "final_response": str(response),
            "intent": "ok"
        }

    except Exception as e:
        return {
            "final_response": "AI error",
            "intent": "failed"
        }