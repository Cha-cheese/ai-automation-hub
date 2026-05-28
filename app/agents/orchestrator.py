from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def automation_graph(state):
    try:
        user_input = state.get("user_input", "")

        # SIMPLE SAFE PROMPT (no LangGraph dependency)
        prompt = f"Answer this user: {user_input}"

        response = llm.invoke(prompt)

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