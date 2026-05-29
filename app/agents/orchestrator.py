from app.agents.llm import build_model

client = build_model()


MODEL_PRIORITY = [
    "gemini-1.5-pro",
    "gemini-1.5-flash"
]


def automation_graph(state):

    user_input = state.get("user_input", "")

    if client is None:
        return {
            "result": "[NO GEMINI CLIENT]",
            "intent": "mock"
        }

    last_error = None

    for model_name in MODEL_PRIORITY:

        try:

            response = client.models.generate_content(
                model=model_name,
                contents=user_input
            )

            return {
                "result": response.text,
                "intent": "success",
                "model_used": model_name
            }

        except Exception as e:
            last_error = str(e)
            continue

    return {
        "result": f"[AI ERROR] {last_error}",
        "intent": "error"
    }