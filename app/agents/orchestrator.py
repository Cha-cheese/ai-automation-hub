from app.agents.llm import build_model

client = build_model()


def automation_graph(state):

    user_input = state.get("user_input", "")

    if client is None:
        return {
            "result": "[NO GEMINI CLIENT]",
            "intent": "mock"
        }

    try:

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_input
        )

        return {
            "result": response.text,
            "intent": "success"
        }

    except Exception as e:

        return {
            "result": f"[AI ERROR] {str(e)}",
            "intent": "error"
        }