from app.agents.llm import build_model

client = build_model()

MODEL = "gemini-1.0-pro"


def automation_graph(state):

    try:
        user_input = state.get("user_input", "")

        if client is None:
            return {
                "result": "[NO GEMINI CLIENT]",
                "intent": "mock"
            }

        response = client.models.generate_content(
            model=MODEL,
            contents=user_input
        )

        return {
            "result": response.text,
            "intent": "success"
        }

    except Exception as e:

        # 🔥 สำคัญมาก: กัน crash 100%
        return {
            "result": f"[AI ERROR SAFE]: {str(e)}",
            "intent": "error"
        }
    
MODEL_PRIORITY = [
    "gemini-1.0-pro"
]