from app.agents.llm import build_model

model = build_model()


def automation_graph(state):

    user_input = state.get("user_input", "")

    if model is None:
        return {
            "result": "[NO MODEL LOADED]",
            "intent": "mock"
        }

    try:

        response = model.generate_content(user_input)

        return {
            "result": response.text,
            "intent": "success"
        }

    except Exception as e:

        return {
            "result": f"[AI ERROR] {str(e)}",
            "intent": "error"
        }