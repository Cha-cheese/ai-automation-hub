from app.agents.llm import build_gemini_llm

genai = build_gemini_llm()


def automation_graph(state):

    user_input = state.get("user_input", "")

    if genai is None:
        return {
            "result": "[MOCK] Gemini not loaded",
            "intent": "mock"
        }

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")

        response = model.generate_content(user_input)

        return {
            "result": response.text,
            "intent": "success"
        }

    except Exception as e:

        print("LLM ERROR:", str(e))

        return {
            "result": f"[AI ERROR FALLBACK] {user_input}",
            "intent": "fallback"
        }