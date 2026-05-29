from app.agents.llm import build_gemini_llm

llm = build_gemini_llm()


def automation_graph(state):

    user_input = state.get("user_input", "")

    # 🔥 fallback mode ถ้า AI พัง
    if llm is None:
        return {
            "result": f"[MOCK RESPONSE] You said: {user_input}",
            "intent": "mock"
        }

    try:
        response = llm.invoke(user_input)

        return {
            "result": str(response),
            "intent": "success"
        }

    except Exception as e:

        # 🔥 IMPORTANT DEBUG
        print("LLM ERROR:", str(e))

        return {
            "result": f"[AI ERROR FALLBACK] {user_input}",
            "intent": "fallback"
        }