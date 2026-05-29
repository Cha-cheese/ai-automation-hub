from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def automation_graph(state):

    user_input = state.get("user_input", "")

    # 🔥 FALLBACK MODE
    if llm is None:

        return {
            "result": f"[MOCK RESPONSE] You said: {user_input}",
            "intent": "mock"
        }

    try:

        # ✅ REAL GEMINI CALL
        response = llm.generate_content(user_input)

        result_text = response.text

        return {
            "result": result_text,
            "intent": "success"
        }

    except Exception as e:

        print("LLM ERROR:", str(e))

        return {
            "result": f"[AI ERROR FALLBACK] {user_input}",
            "intent": "fallback"
        }