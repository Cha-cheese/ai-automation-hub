from app.agents.llm import call_gemini


def automation_graph(state):

    user_input = state.get("user_input", "")

    try:

        result = call_gemini(user_input)

        return {
            "result": result,
            "intent": "success"
        }

    except Exception as e:

        return {
            "result": f"[SYSTEM ERROR]: {str(e)}",
            "intent": "error"
        }