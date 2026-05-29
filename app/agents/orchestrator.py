from app.agents.llm import call_ai


def automation_graph(state):

    user_input = state.get("user_input", "")

    result = call_ai(user_input)

    return {
        "result": result,
        "intent": "success"
    }