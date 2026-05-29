from app.agents.llm import call_gemini


def automation_graph(state):

    try:

        user_input = state.get("user_input", "")

        result = call_gemini(user_input)

        return {
            "result": result,
            "intent": "success"
        }

    except Exception as e:

        return {
            "result": f"[AI ERROR]: {str(e)}",
            "intent": "error"
        }