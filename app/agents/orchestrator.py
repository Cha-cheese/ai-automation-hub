from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def automation_graph(state):
    try:
        user_input = state.get("user_input", "")

        # fallback ถ้าไม่มี key
        if llm is None:
            return {
                "final_response": "LLM not configured",
                "intent": "no_llm"
            }

        response = llm.invoke(user_input)

        return {
            "final_response": str(response),
            "intent": "success"
        }

    except Exception as e:
        return {
            "final_response": "AI processing failed",
            "error": str(e),
            "intent": "failed"
        }